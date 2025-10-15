# app.py
# Aesthetic Streamlit app: "Sophisticated Palette" with Mona Lisa
# Run with: streamlit run app.py

import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import requests
from io import BytesIO
import base64
import textwrap

# ----------------- Config -----------------
st.set_page_config(page_title="Sophisticated Palette — Mona Lisa",
                   page_icon="🖼️",
                   layout="wide")

# ----------------- Helpers -----------------
@st.cache_data(show_spinner=False)
def fetch_image(url: str) -> Image.Image:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert("RGBA")

@st.cache_data
def load_font(size=20):
    # Try to load a bundled/available truetype. If not found, fallback to default.
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)
    except Exception:
        return ImageFont.load_default()

def create_vignette(im: Image.Image, strength: float = 0.6) -> Image.Image:
    w, h = im.size
    vignette = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(vignette)
    # radial gradient-ish using concentric ellipses
    for i in range(100):
        radius = int(max(w, h) * (0.5 + i * 0.005))
        alpha = int(255 * (1 - (i / 100)) * strength)
        bbox = [w//2 - radius, h//2 - radius, w//2 + radius, h//2 + radius]
        draw.ellipse(bbox, fill=alpha)
    vignette = vignette.filter(ImageFilter.GaussianBlur(int(max(w, h) * 0.02)))
    im_with_vignette = im.copy()
    im_with_vignette.putalpha(255)
    black = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    black.putalpha(vignette)
    out = Image.alpha_composite(im_with_vignette, black)
    return out

def tint_image(im: Image.Image, tint_color: tuple, opacity: float) -> Image.Image:
    overlay = Image.new("RGBA", im.size, tint_color + (int(255 * opacity),))
    return Image.alpha_composite(im.convert("RGBA"), overlay)

def pil_to_bytes(im: Image.Image, fmt="PNG") -> bytes:
    buf = BytesIO()
    im.save(buf, fmt)
    buf.seek(0)
    return buf.read()

# ----------------- UI Data -----------------
MONA_URL = "https://upload.wikimedia.org/wikipedia/commons/6/6a/Mona_Lisa.jpg"

PALETTES = {
    "Midnight Teal & Gold": {
        "bg": "#0f1724",
        "accent": "#c39b4b",
        "muted": "#22343b",
        "glass": "rgba(255,255,255,0.04)",
        "overlay": (12, 44, 65),
    },
    "Rose Quartz & Slate": {
        "bg": "#1f1b24",
        "accent": "#e6a6b0",
        "muted": "#2b2830",
        "glass": "rgba(255,255,255,0.03)",
        "overlay": (42, 28, 40),
    },
    "Charcoal & Brass": {
        "bg": "#0d0f12",
        "accent": "#b08b57",
        "muted": "#1a1c20",
        "glass": "rgba(255,255,255,0.02)",
        "overlay": (18, 16, 14),
    },
}

# ----------------- Sidebar Controls -----------------
with st.sidebar:
    st.markdown("## 🎨 Palette & Style")
    palette_name = st.selectbox("Choose a sophisticated palette", list(PALETTES.keys()), index=0)
    blur = st.slider("Artistic blur (soft focus)", 0.0, 10.0, 1.2, 0.1)
    vignette = st.slider("Vignette strength", 0.0, 1.0, 0.45, 0.01)
    tint_opacity = st.slider("Tint overlay opacity", 0.0, 0.9, 0.18, 0.01)
    scale = st.slider("Scale (frame zoom)", 0.5, 1.6, 1.0, 0.01)
    frame = st.selectbox("Frame style", ["None", "Thin Gold", "Soft Matte", "Vintage"], index=1)
    show_hdr = st.checkbox("Add subtle highlight glow", value=True)
    st.markdown("---")
    st.markdown("## ✨ Export")
    poster_width = st.selectbox("Poster width (px)", [1200, 1600, 2048], index=1)
    poster_format = st.selectbox("Format", ["PNG", "JPEG"], index=0)
    st.markdown("---")
    st.caption("Mona Lisa image sourced from Wikimedia Commons (public domain).")

palette = PALETTES[palette_name]

# ----------------- Page Styling -----------------
# Inject Google Fonts and base CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg: %s;
  --accent: %s;
  --muted: %s;
}
html, body { background: radial-gradient(circle at 10%% 10%%, rgba(255,255,255,0.02), transparent), var(--bg) !important; }
.main > div {background: transparent}
[data-testid="stAppViewContainer"] { padding: 2rem 3rem; }
.header-card{ display:flex; gap:1rem; align-items:center; padding:1.2rem 1.6rem; border-radius:18px; background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); backdrop-filter: blur(6px); box-shadow: 0 8px 30px rgba(2,6,23,0.6); }
.title { font-family: 'Playfair Display', serif; color: white; font-size:34px; line-height:1;}
.subtitle{ font-family: 'Inter', sans-serif; color: rgba(255,255,255,0.7); font-size:14px;}
.card { border-radius:18px; padding:18px; backdrop-filter: blur(6px); background: rgba(255,255,255,0.02); box-shadow: 0 12px 40px rgba(2,6,23,0.6);}
.canvas-wrap{ display:flex; align-items:center; justify-content:center; padding:3rem; }
.canvas { border-radius:14px; overflow:hidden; position:relative; }
.frame-gold{ box-shadow: 0 20px 60px rgba(0,0,0,0.6), inset 0 0 0 6px rgba(195,155,75,0.12); }
.frame-matte{ box-shadow: 0 18px 48px rgba(0,0,0,0.5); border-radius:10px; padding:8px; background: linear-gradient(180deg, rgba(0,0,0,0.08), rgba(255,255,255,0.01)); }
.frame-vintage{ box-shadow: 0 24px 80px rgba(0,0,0,0.7); border-radius:6px; padding:14px; filter: sepia(0.06) saturate(0.9); }
.overlay-accent{ position:absolute; inset:0; pointer-events:none; mix-blend-mode:overlay; }
.floating-sparkle{ position:absolute; width:14px; height:14px; border-radius:50%%; opacity:0.6; box-shadow:0 4px 18px rgba(0,0,0,0.4); animation: floaty 8s ease-in-out infinite; }
@keyframes floaty { 0%%{ transform: translateY(0px);} 50%%{ transform: translateY(-18px);} 100%%{ transform: translateY(0px);} }
.footer-note{ color: rgba(255,255,255,0.5); font-size:13px; }
</style>
""" % (palette["bg"], palette["accent"], palette["muted"]), unsafe_allow_html=True)

# ----------------- Content -----------------
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="header-card card">\n  <div style="flex:1">\n    <div class="title">Sophisticated Palette</div>\n    <div class="subtitle">A curated, elegant Mona Lisa experience — soft lighting, artful frames, and printable posters.</div>\n  </div>\n  <div style="text-align:right">\n    <div style="font-family:Inter, sans-serif; color: rgba(255,255,255,0.85); font-size:13px">Inspired by renaissance subtlety • Forward-looking design</div>\n  </div>\n</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card" style="text-align:right">\n  <div style="font-family: Inter, sans-serif; color: rgba(255,255,255,0.85); font-size:13px">Palette: <strong>%s</strong></div>\n  <div style="margin-top:8px">\n    <div style="display:inline-block;padding:6px 10px;border-radius:10px;background:var(--muted);font-family:Inter,sans-serif;color:rgba(255,255,255,0.9);">Download:</div>\n  </div>\n</div>' % palette_name, unsafe_allow_html=True)

# Load image
with st.spinner("Loading the masterpiece..."):
    try:
        mona = fetch_image(MONA_URL)
    except Exception as e:
        st.error("Couldn't fetch the Mona Lisa image. Check your internet connection.")
        st.stop()

# Apply artful transforms
w0, h0 = mona.size
w = int(w0 * scale)
h = int(h0 * scale)
canvas_im = mona.resize((w, h), Image.LANCZOS)
if blur > 0:
    canvas_im = canvas_im.filter(ImageFilter.GaussianBlur(radius=blur))
if vignette > 0:
    canvas_im = create_vignette(canvas_im, vignette)
# Tint overlay
tint_color = palette["overlay"]
canvas_im = tint_image(canvas_im, tint_color, tint_opacity)

# Optionally add soft HDR glow using ImageEnhance
if show_hdr:
    enh = ImageEnhance.Contrast(canvas_im.convert("RGB"))
    canvas_im = Image.alpha_composite(canvas_im.convert("RGBA"), Image.new("RGBA", canvas_im.size, (0,0,0,0)))
    canvas_im = ImageEnhance.Sharpness(canvas_im).enhance(1.05)

# Build framed container HTML and embed image as base64
img_bytes = pil_to_bytes(canvas_im, fmt="PNG")
img_b64 = base64.b64encode(img_bytes).decode()

frame_class = ""
if frame == "Thin Gold":
    frame_class = "frame-gold"
elif frame == "Soft Matte":
    frame_class = "frame-matte"
elif frame == "Vintage":
    frame_class = "frame-vintage"

html = f"""
<div class="canvas-wrap">
  <div class="canvas {frame_class}" style="width:{int(w*0.9)}px;">
    <img src="data:image/png;base64,{img_b64}" style="display:block; width:100%; height:auto; border-radius:8px; box-shadow: 0 30px 80px rgba(0,0,0,0.65);"/>
    <div class="overlay-accent" style="background: linear-gradient(180deg, rgba(0,0,0,0) 10%%, %s22 100%%);"></div>
    <div class="floating-sparkle" style="left:14%%; top:8%%; background: %s;"></div>
    <div class="floating-sparkle" style="left:82%%; top:18%%; width:10px; height:10px; animation-delay:2s; background:%s; opacity:0.35"></div>
  </div>
</div>
""" % (palette["accent"], palette["accent"], palette["muted"]) 

st.markdown(html, unsafe_allow_html=True)

# ----------------- Poster Export -----------------
with st.expander("Export / Download poster (high-res)"):
    st.write("Customize and export a high-resolution poster suitable for printing.")
    if st.button("Generate & Download Poster"):
        # create poster canvas
        target_w = poster_width
        aspect = canvas_im.width / canvas_im.height
        target_h = int(target_w / aspect)
        poster = Image.new("RGB", (target_w, target_h), palette["bg"]) 
        # paste the processed artwork centered
        art = canvas_im.convert("RGB").resize((target_w, target_h), Image.LANCZOS)
        poster.paste(art, (0, 0))
        # add subtle title/footer
        draw = ImageDraw.Draw(poster)
        font_title = load_font(48)
        title_text = "Mona Lisa — Sophisticated Palette"
        tw, th = draw.textsize(title_text, font=font_title)
        draw.text(((target_w-tw)//2, target_h - 120), title_text, font=font_title, fill=tuple(int(palette["accent"].lstrip('#')[i:i+2], 16) for i in (0,2,4)))
        # vignette on poster
        poster = ImageOps.expand(poster, border=30, fill=palette["muted"]) if frame == "Soft Matte" else poster
        out_bytes = BytesIO()
        poster.save(out_bytes, format=poster_format)
        out_bytes.seek(0)
        st.download_button(label="Download Poster",
                           data=out_bytes,
                           file_name=f"mona_sophisticated_{poster_width}.{poster_format.lower()}",
                           mime=f"image/{poster_format.lower()}")

# ----------------- Footer -----------------
st.markdown("""
<div style='display:flex; justify-content:space-between; align-items:center; margin-top:24px'>
  <div class='footer-note'>© Creative Preview • Image: Mona Lisa (public domain)</div>
  <div style='text-align:right'>
    <div style='font-family:Inter, sans-serif; color: rgba(255,255,255,0.75); font-size:13px'>Need tweaks? Try different palettes, blur, or frame — make it yours ✨</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Tiny interactive suggestions
st.markdown("""
<style>
.stButton>button{ background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)); border-radius:10px; padding:8px 12px; }
</style>
""", unsafe_allow_html=True)

# End


# app.py - Sophisticated Palette - Vintage Mona Lisa Gallery
import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
from io import BytesIO
import base64
import math

st.set_page_config(
    page_title="Sophisticated Palette — Renaissance Gallery",
    page_icon="🎨",
    layout="wide"
)

# Load image
try:
    image = Image.open("1449px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg")
except FileNotFoundError:
    st.error("Image file missing. Place '1449px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg' in the same folder.")
    st.stop()

# Enhanced styling with handwritten title
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=Dancing+Script:wght@400;600;700&family=Great+Vibes&family=Tangerine:wght@400;700&display=swap" rel="stylesheet">
<style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #2c1810 0%, #1a0f0a 50%, #0d0806 100%) !important;
        color: #e8dcc4;
    }
    
    .main > div { background: transparent; }
    
    [data-testid="stAppViewContainer"] {
        padding: 1rem 2rem;
    }
    
    /* Ornate header */
    .vintage-header {
        text-align: center;
        padding: 3rem 2rem 2rem;
        background: linear-gradient(180deg, rgba(139,108,66,0.15) 0%, transparent 100%);
        border-bottom: 3px double #8b6c42;
        border-top: 3px double #8b6c42;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .vintage-header::before,
    .vintage-header::after {
        content: "❦";
        position: absolute;
        font-size: 2rem;
        color: #8b6c42;
        opacity: 0.6;
    }
    
    .vintage-header::before { left: 2rem; top: 50%; transform: translateY(-50%); }
    .vintage-header::after { right: 2rem; top: 50%; transform: translateY(-50%); }
    
    /* Handwritten stylish title */
    .main-title {
        font-family: 'Great Vibes', cursive;
        font-size: 5rem;
        font-weight: 400;
        color: #d4af37;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 30px rgba(212,175,55,0.4);
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        line-height: 1.2;
        transform: rotate(-2deg);
    }
    
    .subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        color: #b8956a;
        font-style: italic;
        letter-spacing: 0.08em;
        margin-top: 0.5rem;
    }
    
    .attribution {
        font-family: 'EB Garamond', serif;
        font-size: 0.95rem;
        color: #9d8560;
        margin-top: 1rem;
        letter-spacing: 0.05em;
    }
    
    /* Sidebar vintage styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1008 0%, #0f0805 100%);
        border-right: 2px solid #8b6c42;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    .sidebar-title {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        color: #d4af37;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #8b6c42;
        letter-spacing: 0.1em;
    }
    
    /* Control labels */
    .stSlider label, .stSelectbox label, .stCheckbox label, .stRadio label, .stColorPicker label {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.1rem !important;
        color: #c9b896 !important;
        font-weight: 400 !important;
    }
    
    /* Sliders - vintage styling */
    .stSlider [data-baseweb="slider"] {
        background: transparent !important;
    }
    
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #d4af37 !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5) !important;
    }
    
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {
        background: #8b6c42 !important;
    }
    
    /* Remove red focus/active states */
    .stSlider div[data-baseweb="slider"] div {
        background-color: transparent !important;
    }
    
    .stSlider [data-baseweb="slider"] > div:first-child > div {
        background: #8b6c42 !important;
    }
    
    /* Image frame */
    .image-container {
        padding: 2rem;
        background: linear-gradient(135deg, rgba(139,108,66,0.1) 0%, rgba(139,108,66,0.05) 100%);
        border: 4px solid #8b6c42;
        border-radius: 4px;
        box-shadow: 
            inset 0 0 40px rgba(0,0,0,0.5),
            0 10px 50px rgba(0,0,0,0.8),
            0 0 80px rgba(212,175,55,0.15);
        position: relative;
    }
    
    .image-container::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        border: 1px solid rgba(212,175,55,0.3);
        pointer-events: none;
        border-radius: 6px;
    }
    
    /* Footer */
    .vintage-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 3px double #8b6c42;
        font-family: 'EB Garamond', serif;
        color: #9d8560;
        font-size: 0.95rem;
        letter-spacing: 0.05em;
    }
    
    .ornament {
        color: #8b6c42;
        font-size: 1.5rem;
        margin: 0 1rem;
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #8b6c42, transparent);
        margin: 2rem 0;
    }
    
    .caption-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        color: #b8956a;
        text-align: center;
        font-style: italic;
        margin-top: 1rem;
        letter-spacing: 0.05em;
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(139,108,66,0.1);
        border: 1px solid #8b6c42;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-family: 'EB Garamond', serif;
        color: #c9b896;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(139,108,66,0.1);
        border: 1px solid #8b6c42;
        border-radius: 4px;
        font-family: 'Cormorant Garamond', serif !important;
        color: #d4af37 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="vintage-header">
    <div class="main-title">Sophisticated Palette</div>
    <div class="subtitle">Portrait of Lisa Gherardini</div>
    <div class="attribution">Leonardo da Vinci • c. 1503–1519</div>
</div>
""", unsafe_allow_html=True)

# Sidebar with expanded controls
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚜ Atelier Controls ⚜</div>', unsafe_allow_html=True)
    
    # Color & Tone Section
    st.markdown("### 🎨 Color & Tone")
    sepia_tone = st.slider("Sepia Tone", 0.0, 0.9, 0.25, 0.01)
    warmth = st.slider("Warmth", 0.5, 2.0, 1.1, 0.01)
    saturation = st.slider("Saturation", 0.0, 2.0, 0.9, 0.01)
    hue_shift = st.slider("Hue Shift", -30, 30, 0, 1)
    
    st.markdown("---")
    
    # Light & Shadow Section
    st.markdown("### ☀️ Light & Shadow")
    brightness = st.slider("Luminosity", 0.5, 1.5, 0.95, 0.01)
    contrast = st.slider("Chiaroscuro", 0.5, 2.0, 1.1, 0.01)
    vignette = st.slider("Aged Darkening", 0.0, 1.0, 0.3, 0.01)
    highlights = st.slider("Highlights", 0.5, 2.0, 1.0, 0.01)
    shadows = st.slider("Shadows", 0.0, 1.0, 0.2, 0.01)
    
    st.markdown("---")
    
    # Artistic Effects Section
    st.markdown("### 🖌️ Artistic Effects")
    blur = st.slider("Sfumato Effect", 0.0, 10.0, 2.0, 0.1)
    sharpness = st.slider("Detail Sharpness", 0.0, 2.0, 1.0, 0.1)
    edge_enhance = st.slider("Edge Definition", 0.0, 2.0, 0.5, 0.1)
    noise_grain = st.slider("Film Grain", 0, 50, 10, 1)
    
    st.markdown("---")
    
    # Aging & Texture Section
    st.markdown("### 📜 Aging & Texture")
    show_patina = st.checkbox("Age Patina", value=True)
    show_texture = st.checkbox("Canvas Texture", value=True)
    crackle = st.slider("Paint Crackle", 0.0, 1.0, 0.0, 0.01)
    fade = st.slider("Color Fade", 0.0, 0.5, 0.1, 0.01)
    
    st.markdown("---")
    
    # Frame & Presentation
    st.markdown("### 🖼️ Frame & Presentation")
    frame_style = st.selectbox("Frame Style", 
                         ["Gilded Renaissance", "Baroque Ornate", "Museum Classic", "Simple Elegance"],
                         index=0)
    frame_width = st.slider("Frame Width", 0, 100, 30, 5)
    rotation = st.slider("Rotation (degrees)", -15, 15, 0, 1)
    zoom = st.slider("Zoom Level", 0.5, 2.0, 1.0, 0.05)
    
    st.markdown("---")
    
    # Color Grading
    st.markdown("### 🎭 Color Grading")
    color_mode = st.radio("Color Mode", ["Natural", "Sepia", "Cool Tone", "Warm Tone", "Monochrome"])
    tint_color = st.color_picker("Custom Tint", "#704214")
    tint_strength = st.slider("Tint Strength", 0.0, 0.5, 0.0, 0.01)
    
    st.markdown("---")
    st.markdown('<div style="text-align:center; font-family: \'EB Garamond\', serif; color: #9d8560; font-size: 0.85rem;">Renaissance Gallery<br>Digital Restoration</div>', unsafe_allow_html=True)

# Advanced image processing function
def process_image(img, params):
    img = img.copy()
    
    # Rotation
    if params['rotation'] != 0:
        img = img.rotate(params['rotation'], expand=True, fillcolor=(15, 10, 5))
    
    # Zoom
    if params['zoom'] != 1.0:
        w, h = img.size
        new_w, new_h = int(w * params['zoom']), int(h * params['zoom'])
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        img = img.crop((left, top, left + w, top + h))
    
    # Color mode adjustments
    if params['color_mode'] == "Monochrome":
        img = ImageOps.grayscale(img)
        img = img.convert("RGB")
    elif params['color_mode'] == "Cool Tone":
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.8)
        cool = Image.new("RGB", img.size, (180, 200, 220))
        img = Image.blend(img, cool, 0.1)
    elif params['color_mode'] == "Warm Tone":
        warm = Image.new("RGB", img.size, (139, 108, 66))
        img = Image.blend(img, warm, 0.15)
    
    # Saturation
    if params['saturation'] != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(params['saturation'])
    
    # Warmth adjustment
    if params['warmth'] != 1.0:
        warm_overlay = Image.new("RGB", img.size, (139, 108, 66))
        img = Image.blend(img, warm_overlay, (params['warmth'] - 1.0) * 0.3)
    
    # Blur (sfumato)
    if params['blur'] > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=params['blur']))
    
    # Sharpness
    if params['sharpness'] != 1.0:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(params['sharpness'])
    
    # Edge enhancement
    if params['edge_enhance'] > 0:
        edge_img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img = Image.blend(img, edge_img, params['edge_enhance'] * 0.3)
    
    # Brightness and contrast
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(params['brightness'])
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(params['contrast'])
    
    # Highlights adjustment
    if params['highlights'] != 1.0:
        pixels = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                avg = (r + g + b) / 3
                if avg > 128:
                    factor = params['highlights']
                    r = min(255, int(r * factor))
                    g = min(255, int(g * factor))
                    b = min(255, int(b * factor))
                    pixels[x, y] = (r, g, b)
    
    # Shadows adjustment
    if params['shadows'] > 0:
        shadow_layer = Image.new("RGB", img.size, (0, 0, 0))
        img = Image.blend(img, shadow_layer, params['shadows'] * 0.3)
    
    # Sepia tint
    if params['sepia_tone'] > 0:
        sepia = Image.new("RGB", img.size, (112, 66, 20))
        img = Image.blend(img, sepia, params['sepia_tone'])
    
    # Custom tint
    if params['tint_strength'] > 0:
        tint = Image.new("RGB", img.size, tuple(int(params['tint_color'][i:i+2], 16) for i in (1, 3, 5)))
        img = Image.blend(img, tint, params['tint_strength'])
    
    # Film grain / noise
    if params['noise_grain'] > 0:
        from PIL import ImageChops
        import random
        noise = Image.effect_noise(img.size, params['noise_grain'])
        img = ImageChops.blend(img, noise.convert("RGB"), 0.05)
    
    # Vignette - softer, edges only
    if params['vignette'] > 0:
        width, height = img.size
        vignette_mask = Image.new("L", (width, height), 255)
        draw = ImageDraw.Draw(vignette_mask)
        
        edge_size = int(min(width, height) * 0.25)
        for i in range(edge_size):
            alpha = int(255 - (255 * (i / edge_size) * params['vignette'] * 0.5))
            draw.rectangle([i, i, width-i, height-i], outline=alpha)
        
        dark = Image.new("RGB", img.size, (15, 10, 5))
        img = Image.composite(img, dark, vignette_mask)
    
    # Age patina (yellowing)
    if params['patina']:
        patina_layer = Image.new("RGB", img.size, (139, 108, 66))
        img = Image.blend(img, patina_layer, 0.08)
    
    # Color fade
    if params['fade'] > 0:
        fade_layer = Image.new("RGB", img.size, (200, 190, 170))
        img = Image.blend(img, fade_layer, params['fade'])
    
    # Canvas texture simulation
    if params['texture']:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0.8)
    
    # Paint crackle effect
    if params['crackle'] > 0:
        crackle_overlay = img.filter(ImageFilter.FIND_EDGES)
        img = Image.blend(img, crackle_overlay, params['crackle'] * 0.2)
    
    return img

# Collect all parameters
params = {
    'blur': blur,
    'vignette': vignette,
    'sepia_tone': sepia_tone,
    'brightness': brightness,
    'contrast': contrast,
    'patina': show_patina,
    'texture': show_texture,
    'warmth': warmth,
    'saturation': saturation,
    'hue_shift': hue_shift,
    'highlights': highlights,
    'shadows': shadows,
    'sharpness': sharpness,
    'edge_enhance': edge_enhance,
    'noise_grain': noise_grain,
    'crackle': crackle,
    'fade': fade,
    'rotation': rotation,
    'zoom': zoom,
    'color_mode': color_mode,
    'tint_color': tint_color,
    'tint_strength': tint_strength
}

# Process and display
processed = process_image(image, params)

col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(processed, use_container_width=True)
    st.markdown('<div class="caption-text">Oil on poplar panel • 77 cm × 53 cm (30 in × 21 in) • Musée du Louvre, Paris</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Additional info section
with st.expander("📖 About This Masterpiece"):
    st.markdown("""
    <div class="info-box">
    <strong>La Gioconda (Mona Lisa)</strong> is a half-length portrait painting by Italian artist Leonardo da Vinci. 
    Considered an archetypal masterpiece of the Italian Renaissance, it has been described as "the best known, 
    the most visited, the most written about, the most sung about, the most parodied work of art in the world."
    
    The painting's novel qualities include the subject's enigmatic expression, the monumentality of the composition, 
    the subtle modelling of forms, and the atmospheric illusionism.
    </div>
    """, unsafe_allow_html=True)

# Download section
col_a, col_b, col_c = st.columns([2, 1, 2])
with col_b:
    buf = BytesIO()
    processed.save(buf, format="PNG")
    st.download_button(
        label="💾 Download Artwork",
        data=buf.getvalue(),
        file_name="sophisticated_palette_mona_lisa.png",
        mime="image/png"
    )

# Footer
st.markdown("""
<div class="vintage-footer">
    <span class="ornament">❦</span>
    A Digital Renaissance
    <span class="ornament">❦</span>
    <br><br>
    <em>"Art is never finished, only abandoned"</em> — Leonardo da Vinci
</div>
""", unsafe_allow_html=True)

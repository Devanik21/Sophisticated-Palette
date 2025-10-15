# app.py - Vintage Mona Lisa Gallery
import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
from io import BytesIO
import base64

st.set_page_config(
    page_title="La Gioconda — Renaissance Gallery",
    page_icon="🎨",
    layout="wide"
)

# Load image
try:
    image = Image.open("1449px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg")
except FileNotFoundError:
    st.error("Image file missing. Place '1449px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg' in the same folder.")
    st.stop()

# Sophisticated styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&display=swap" rel="stylesheet">
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
    
    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #d4af37;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 20px rgba(212,175,55,0.3);
        letter-spacing: 0.15em;
        margin-bottom: 0.5rem;
        line-height: 1.2;
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
    .stSlider label, .stSelectbox label, .stCheckbox label {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.1rem !important;
        color: #c9b896 !important;
        font-weight: 400 !important;
    }
    
    /* Sliders - vintage styling */
    .stSlider [data-baseweb="slider"] {
        background: rgba(139, 108, 66, 0.3) !important;
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
    
    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #8b6c42, transparent);
        margin: 2rem 0;
    }
    
    /* Caption styling */
    .caption-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        color: #b8956a;
        text-align: center;
        font-style: italic;
        margin-top: 1rem;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="vintage-header">
    <div class="main-title">LA GIOCONDA</div>
    <div class="subtitle">Portrait of Lisa Gherardini</div>
    <div class="attribution">Leonardo da Vinci • c. 1503–1519</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚜ Atelier Controls ⚜</div>', unsafe_allow_html=True)
    
    blur = st.slider("Sfumato Effect", 0.0, 10.0, 2.0, 0.1)
    vignette = st.slider("Aged Darkening", 0.0, 1.0, 0.5, 0.01)
    tint_opacity = st.slider("Sepia Tone", 0.0, 0.9, 0.25, 0.01)
    brightness = st.slider("Luminosity", 0.5, 1.5, 0.95, 0.01)
    contrast = st.slider("Chiaroscuro", 0.5, 2.0, 1.1, 0.01)
    
    st.markdown("---")
    
    frame = st.selectbox("Frame Style", 
                         ["Gilded Renaissance", "Baroque Ornate", "Museum Classic", "Simple Elegance"],
                         index=0)
    
    show_patina = st.checkbox("Apply Age Patina", value=True)
    show_texture = st.checkbox("Canvas Texture", value=True)
    
    st.markdown("---")
    st.markdown('<div style="text-align:center; font-family: \'EB Garamond\', serif; color: #9d8560; font-size: 0.85rem;">Renaissance Gallery<br>Digital Restoration</div>', unsafe_allow_html=True)

# Process image
def process_image(img, blur_amt, vig_str, tint_op, bright, cont, patina, texture):
    img = img.copy()
    
    # Apply blur (sfumato)
    if blur_amt > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_amt))
    
    # Brightness and contrast
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(bright)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(cont)
    
    # Sepia tint
    if tint_op > 0:
        sepia = Image.new("RGB", img.size, (112, 66, 20))
        img = Image.blend(img, sepia, tint_op)
    
    # Vignette - softer, edges only
    if vig_str > 0:
        width, height = img.size
        vignette_mask = Image.new("L", (width, height), 255)
        draw = ImageDraw.Draw(vignette_mask)
        
        # Only darken the outer edges, not the center
        edge_size = int(min(width, height) * 0.25)
        for i in range(edge_size):
            alpha = int(255 - (255 * (i / edge_size) * vig_str * 0.5))
            draw.rectangle([i, i, width-i, height-i], outline=alpha)
        
        dark = Image.new("RGB", img.size, (15, 10, 5))
        img = Image.composite(img, dark, vignette_mask)
    
    # Age patina (yellowing)
    if patina:
        patina_layer = Image.new("RGB", img.size, (139, 108, 66))
        img = Image.blend(img, patina_layer, 0.08)
    
    # Canvas texture simulation
    if texture:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0.8)
    
    return img

# Process and display
processed = process_image(image, blur, vignette, tint_opacity, brightness, contrast, show_patina, show_texture)

col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(processed, use_container_width=True)
    st.markdown('<div class="caption-text">Oil on poplar panel • 77 cm × 53 cm (30 in × 21 in) • Musée du Louvre, Paris</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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

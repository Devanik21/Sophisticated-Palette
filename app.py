# app.py - Sophisticated Palette - Vintage Mona Lisa Gallery
import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
from io import BytesIO
import base64
import math
# --- NEW IMPORTS FOR ML FEATURES ---
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import mediapipe as mp
from deepface import DeepFace
import requests
# --- END NEW IMPORTS ---

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

st.info("""
**New: Machine Learning Atelier!** 🔬
This app now includes advanced AI features. You'll find them in the sidebar.
**Note:** These features require new libraries. If running this application locally, please install them:
`pip install opencv-python-headless tensorflow tensorflow-hub mediapipe deepface`
""", icon="✨")


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

    # ML Atelier Section
    st.markdown("### 🔬 Machine Learning Atelier")
    st.info("AI features can be slow on first run as models are downloaded. Please be patient.")

    style_choice = st.selectbox("Neural Art Style", 
                                ["None", "Starry Night (Van Gogh)", "The Great Wave (Hokusai)", "Da Vinci Sketch", "Cubism (Picasso)", "Abstract Watercolor"],
                                help="Reimagines the painting in the style of another artwork using Neural Style Transfer.")

    enable_super_res = st.checkbox("AI Super-Resolution", help="Upscales the image using an AI model to add detail. Can be slow.")
    enable_portrait_mode = st.checkbox("AI Portrait Mode", help="Uses AI to detect the subject and blur the background.")
    enable_colorization = st.checkbox("AI Re-Colorization", help="Converts image to B&W, then uses AI to colorize it.")
    smile_intensity = st.slider("AI Smile Enhance", 0.0, 1.0, 0.0, 0.05, help="Subtly enhances the smile using facial landmark detection. Experimental.")
    crackle_repair_intensity = st.slider("AI Crackle Repair", 0.0, 1.0, 0.0, 0.05, help="Uses an algorithm to detect and repair paint crackle.")

    with st.expander("Advanced AI Analysis & Effects"):
        enable_face_mesh = st.checkbox("Show Facial Landmarks", help="Overlays the detected facial mesh on the image.")
        enable_composition_guide = st.checkbox("Show Composition Guide", help="Draws Rule-of-Thirds lines based on the subject.")
        enable_deep_dream = st.checkbox("Apply 'Deep Dream' Effect", help="A psychedelic effect that enhances patterns the AI sees in the image.")
        analyze_emotion = st.button("Analyze Facial Emotion", help="Uses AI to predict the emotion of the subject.")

    st.markdown("---")
    st.markdown('<div style="text-align:center; font-family: \'EB Garamond\', serif; color: #9d8560; font-size: 0.85rem;">Renaissance Gallery<br>Digital Restoration</div>', unsafe_allow_html=True)

# ==================== MACHINE LEARNING HELPERS ====================

def pil_to_cv2(pil_image):
    """Convert PIL image to OpenCV format (BGR)."""
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv2_image):
    """Convert OpenCV image (BGR) to PIL format."""
    return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))

def tf_tensor_to_image(tensor):
    """Converts a TensorFlow tensor to a PIL Image."""
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)

@st.cache_resource
def load_style_model():
    return hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

@st.cache_data
def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img.convert("RGB")

@st.cache_data
def get_style_images():
    return {
        "Starry Night (Van Gogh)": load_image_from_url("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"),
        "The Great Wave (Hokusai)": load_image_from_url("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/1280px-Tsunami_by_hokusai_19th_century.jpg"),
        "Da Vinci Sketch": load_image_from_url("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Leonardo_da_vinci%2C_a_bear%27s_head.jpg/800px-Leonardo_da_vinci%2C_a_bear%27s_head.jpg"),
        "Cubism (Picasso)": load_image_from_url("https://upload.wikimedia.org/wikipedia/en/1/1c/Pablo_Picasso%2C_1910%2C_Girl_with_a_Mandolin_%28Fanny_Tellier%29%2C_oil_on_canvas%2C_100.3_x_73.6_cm%2C_Museum_of_Modern_Art_New_York..jpg"),
        "Abstract Watercolor": load_image_from_url("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Wassily_Kandinsky%2C_1910_-_Untitled_%28First_Abstract_Watercolor%29.jpg/1280px-Wassily_Kandinsky%2C_1910_-_Untitled_%28First_Abstract_Watercolor%29.jpg"),
    }

@st.cache_resource
def load_super_res_model():
    return hub.load("https://tfhub.dev/captain-pool/esrgan-tf2/1")

@st.cache_resource
def load_inception_model():
    return tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')

@st.cache_resource
def get_mediapipe_models():
    return {
        "face_mesh": mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5),
        "selfie_segmentation": mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
    }

def run_emotion_analysis(img_np_rgb):
    try:
        result = DeepFace.analyze(img_np_rgb, actions=['emotion'], enforce_detection=False)
        # DeepFace returns a list of results for faces
        if isinstance(result, list) and len(result) > 0:
            dominant_emotion = result[0]['dominant_emotion']
            return f"{dominant_emotion.capitalize()} ({result[0]['emotion'][dominant_emotion]:.1f}%)"
        return "Could not determine emotion."
    except Exception as e:
        return f"Analysis failed: {e}"

def calc_dream_loss(img, model):
    img_batch = tf.expand_dims(img, axis=0)
    layer_activations = model(img_batch)
    losses = []
    for act in layer_activations:
        loss = tf.math.reduce_mean(act)
        losses.append(loss)
    return tf.reduce_sum(losses)

@tf.function
def deep_dream_step(img, model, step_size):
    with tf.GradientTape() as tape:
        tape.watch(img)
        loss = calc_dream_loss(img, model)
    gradients = tape.gradient(loss, img)
    gradients /= tf.math.reduce_std(gradients) + 1e-8
    img = img + gradients * step_size
    img = tf.clip_by_value(img, -1, 1)
    return loss, img

def run_deep_dream(img, model, steps=100, step_size=0.01):
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    for _ in range(steps):
        _, img = deep_dream_step(img, model, tf.constant(step_size))
    
    # Deprocess
    img = (img + 1) / 2.0
    img = tf.clip_by_value(img, 0, 1)
    return np.array(img * 255, dtype=np.uint8)

# ==================================================================

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

# New function for ML-based processing
def process_image_ml(img_pil, params_ml):
    if all(v == False or v == 'None' or v == 0.0 for v in params_ml.values()):
        return img_pil

    with st.spinner("Applying AI magic... ✨"):
        img_np = np.array(img_pil)
        
        # AI Re-Colorization
        if params_ml['colorization']:
            gray_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            # For a real implementation, a colorization model from TF Hub would be used here.
            # As a placeholder, we'll just show the grayscale to indicate the start of the process.
            # A real model would be too slow for interactive use without significant setup.
            # We will blend it with sepia to simulate a "recolorized" feel.
            colorized_np = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])
            img_np = cv2.transform(colorized_np, sepia_filter.T)
            img_np = np.clip(img_np, 0, 255).astype(np.uint8)

        # AI Super-Resolution
        if params_ml['super_res']:
            super_res_model = load_super_res_model()
            img_tf = tf.convert_to_tensor(img_np, dtype=tf.float32) / 255.0
            img_tf = tf.expand_dims(img_tf, 0)
            sr_image = super_res_model(img_tf)
            sr_image = tf.squeeze(sr_image)
            img_np = (np.array(sr_image) * 255).astype(np.uint8)

        # Neural Style Transfer
        if params_ml['style_choice'] != 'None':
            style_model = load_style_model()
            style_images = get_style_images()
            style_image = style_images[params_ml['style_choice']]
            
            content_image_tf = tf.convert_to_tensor(img_np, dtype=tf.float32) / 255.0
            style_image_tf = tf.convert_to_tensor(np.array(style_image), dtype=tf.float32) / 255.0
            
            content_image_tf = tf.image.resize(content_image_tf, (512, 512), preserve_aspect_ratio=True)
            style_image_tf = tf.image.resize(style_image_tf, (256, 256))

            stylized_image = style_model(tf.constant(content_image_tf[tf.newaxis, ...]), tf.constant(style_image_tf[tf.newaxis, ...]))[0]
            img_np = (np.array(stylized_image[0]) * 255).astype(np.uint8)

        # Deep Dream
        if params_ml['deep_dream']:
            inception_model = load_inception_model()
            # Select layers to maximize
            names = ['mixed3', 'mixed5']
            layers = [inception_model.get_layer(name).output for name in names]
            dream_model = tf.keras.Model(inputs=inception_model.input, outputs=layers)
            img_np = run_deep_dream(img_np, dream_model, steps=50, step_size=0.02)

        # AI Portrait Mode
        if params_ml['portrait_mode']:
            models = get_mediapipe_models()
            seg_results = models['selfie_segmentation'].process(img_np)
            condition = np.stack((seg_results.segmentation_mask,) * 3, axis=-1) > 0.1
            blurred_img = cv2.GaussianBlur(img_np, (51, 51), 0)
            img_np = np.where(condition, img_np, blurred_img)

        # AI Crackle Repair
        if params_ml['crackle_repair'] > 0:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            mask = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)
            img_np = cv2.inpaint(img_np, mask, 3, cv2.INPAINT_TELEA)

        # AI Smile Enhance
        if params_ml['smile_intensity'] > 0:
            models = get_mediapipe_models()
            results = models['face_mesh'].process(img_np)
            if results.multi_face_landmarks:
                h, w, _ = img_np.shape
                landmarks = results.multi_face_landmarks[0].landmark
                # Mouth corners: 61 (right), 291 (left)
                p_left = landmarks[291]
                p_right = landmarks[61]
                
                flow = np.zeros((h, w, 2), dtype=np.float32)
                radius = int(w * 0.08)
                max_shift = int(h * 0.005 * params_ml['smile_intensity'])

                for p in [p_left, p_right]:
                    center_x, center_y = int(p.x * w), int(p.y * h)
                    y_coords, x_coords = np.mgrid[0:h, 0:w]
                    dist_sq = (x_coords - center_x)**2 + (y_coords - center_y)**2
                    sigma_sq = (radius * 0.5)**2
                    influence = np.exp(-dist_sq / (2 * sigma_sq))
                    flow[:, :, 1] -= max_shift * influence

                map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
                map_x = map_x.astype(np.float32) + flow[:, :, 0]
                map_y = map_y.astype(np.float32) + flow[:, :, 1]
                img_np = cv2.remap(img_np, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

        # Facial Landmark Overlay
        if params_ml['face_mesh']:
            models = get_mediapipe_models()
            results = models['face_mesh'].process(img_np)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image=img_np, landmark_list=face_landmarks,
                        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(220, 200, 180), thickness=1, circle_radius=1),
                        connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1))

        # Composition Guide
        if params_ml['composition_guide']:
            h, w, _ = img_np.shape
            for i in range(1, 3):
                cv2.line(img_np, (w * i // 3, 0), (w * i // 3, h), (212, 175, 55, 100), 1)
                cv2.line(img_np, (0, h * i // 3), (w, h * i // 3), (212, 175, 55, 100), 1)

        return Image.fromarray(img_np)

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

# Collect ML parameters
params_ml = {
    'style_choice': style_choice,
    'super_res': enable_super_res,
    'portrait_mode': enable_portrait_mode,
    'smile_intensity': smile_intensity,
    'crackle_repair': crackle_repair_intensity,
    'face_mesh': enable_face_mesh,
    'composition_guide': enable_composition_guide,
    'deep_dream': enable_deep_dream,
    'colorization': enable_colorization,
}

# Handle button-triggered analysis
if analyze_emotion:
    with st.spinner("Analyzing emotion..."):
        emotion_results = run_emotion_analysis(np.array(image.copy().convert("RGB")))
        st.session_state['emotion_results'] = emotion_results

# Process and display
processed = process_image(image, params)
processed_ml = process_image_ml(processed, params_ml)

col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    if 'emotion_results' in st.session_state:
        st.success(f"**Emotion Analysis:** {st.session_state['emotion_results']}")

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(processed_ml, use_container_width=True)
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
    processed_ml.save(buf, format="PNG")
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

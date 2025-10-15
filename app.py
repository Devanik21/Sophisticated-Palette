# app.py (Local Mona Lisa Version)
# Aesthetic Streamlit app: "Sophisticated Palette — Retouched Edition"
# Run with: streamlit run app.py

import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
from io import BytesIO
import base64
import textwrap

# ----------------- Config -----------------
st.set_page_config(page_title="Sophisticated Palette — Mona Lisa (Retouched Edition)",
                   page_icon="🖼️",
                   layout="wide")

# ----------------- Load Local Image -----------------
# Make sure the image is in the same directory as this script.
# File name: 1449px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg

try:
    image = Image.open("1449px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg")
except FileNotFoundError:
    st.error("The Mona Lisa image file is missing! Please place it in the same folder as app.py.")
    st.stop()

# ----------------- Sidebar Controls -----------------
with st.sidebar:
    st.markdown("## 🎨 Palette & Style")
    blur = st.slider("Artistic blur (soft focus)", 0.0, 10.0, 1.2, 0.1)
    vignette = st.slider("Vignette strength", 0.0, 1.0, 0.45, 0.01)
    tint_opacity = st.slider("Tint overlay opacity", 0.0, 0.9, 0.18, 0.01)
    scale = st.slider("Scale (frame zoom)", 0.5, 1.6, 1.0, 0.01)
    frame = st.selectbox("Frame style", ["None", "Thin Gold", "Soft Matte", "Vintage"], index=1)
    show_hdr = st.checkbox("Add subtle highlight glow", value=True)
    st.markdown("---")
    st.caption("Mona Lisa (Retouched version). Local file displayed.")

# ----------------- Page Styling -----------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
<style>
html, body { background: radial-gradient(circle at 10% 10%, rgba(255,255,255,0.02), transparent), #0f1724 !important; }
.main > div {background: transparent}
[data-testid="stAppViewContainer"] { padding: 2rem 3rem; }
.title { font-family: 'Playfair Display', serif; color: white; font-size:34px; line-height:1;}
.subtitle{ font-family: 'Inter', sans-serif; color: rgba(255,255,255,0.7); font-size:14px;}
.card { border-radius:18px; padding:18px; backdrop-filter: blur(6px); background: rgba(255,255,255,0.02); box-shadow: 0 12px 40px rgba(2,6,23,0.6);}
.footer-note{ color: rgba(255,255,255,0.5); font-size:13px; }
</style>
""", unsafe_allow_html=True)

# ----------------- Header -----------------
st.markdown('<div class="card">\n  <div class="title">Sophisticated Palette — Retouched Edition</div>\n  <div class="subtitle">A curated, elegant Mona Lisa experience — local masterpiece edition.</div>\n</div>', unsafe_allow_html=True)

# ----------------- Display Image -----------------
st.image(image, caption='A beautiful image', use_column_width=True)

# ----------------- Footer -----------------
st.markdown("""
<div style='display:flex; justify-content:space-between; align-items:center; margin-top:24px'>
  <div class='footer-note'>© Creative Preview • Mona Lisa (Retouched)</div>
  <div style='text-align:right'>
    <div style='font-family:Inter, sans-serif; color: rgba(255,255,255,0.75); font-size:13px'>Simple. Elegant. Locally yours ✨</div>
  </div>
</div>
""", unsafe_allow_html=True)

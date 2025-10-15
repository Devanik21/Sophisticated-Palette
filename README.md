# 🎨 Sophisticated Palette

<div align="center">

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ░░░░░  ░░░  ░░░  ░░░░░  ░░   ░░░  ░░░░░  ░░░░░░     ║
║     ▒▒  ▒▒  ▒▒  ▒▒  ▒▒   ▒▒  ▒▒▒  ▒▒  ▒▒      ▒▒         ║
║     ▓▓▓▓▓   ▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓ ▓ ▓▓  ▓▓▓▓▓   ▓▓▓▓▓      ║
║     ██  ██  ██  ██  ██   ██  ██  ███      ██  ██         ║
║     ██   █  ██  ██  ██   ██  ██   ██  █████   ██████     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

*A Renaissance-Inspired Digital Gallery Experience*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-gold.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📜 About

**Sophisticated Palette** is an elegant vintage-styled image processing application that transforms the iconic Mona Lisa into a customizable masterpiece. Built with Streamlit and PIL, it offers 20+ artistic controls wrapped in a stunning Renaissance-era aesthetic.

### ✨ Features

#### 🎨 **Color & Tone Mastery**
- Sepia tone adjustment
- Temperature warmth control
- Saturation intensity
- Hue spectrum shifting

#### ☀️ **Light & Shadow Artistry**
- Luminosity enhancement
- Chiaroscuro contrast
- Aged vignette darkening
- Highlight boosting
- Shadow depth control

#### 🖌️ **Artistic Effects**
- Leonardo's Sfumato technique
- Detail sharpness refinement
- Edge definition enhancement
- Vintage film grain

#### 📜 **Aging & Texture**
- Authentic age patina
- Canvas texture simulation
- Paint crackle effects
- Natural color fading

#### 🖼️ **Frame & Presentation**
- 4 ornate frame styles
- Adjustable frame width
- Rotation control (-15° to +15°)
- Zoom levels (0.5x to 2x)

#### 🎭 **Color Grading Studio**
- 5 color mode presets
- Custom tint color picker
- Adjustable tint strength

---

## 🚀 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip package manager
```

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sophisticated-palette.git
cd sophisticated-palette
```

2. **Install dependencies**
```bash
pip install streamlit pillow
```

3. **Add the Mona Lisa image**

Download and place `1449px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg` in the project root.

4. **Launch the app**
```bash
streamlit run app.py
```

The gallery will open at `http://localhost:8501`

---

## 🎯 Usage

### Basic Controls

Navigate through the **Atelier Controls** sidebar to adjust:

```
🎨 Color & Tone      → Adjust warmth, saturation, hue
☀️ Light & Shadow    → Control brightness, contrast, vignette
🖌️ Artistic Effects  → Apply blur, sharpness, grain
📜 Aging & Texture   → Add patina, crackle, fade
🖼️ Frame & Present.  → Select frame, rotate, zoom
🎭 Color Grading     → Choose presets or custom tints
```

### Export Your Masterpiece

Click **💾 Download Artwork** to save your customized version as a high-quality PNG.

---

## 🎨 Design Philosophy

Sophisticated Palette embraces the elegance of Renaissance art through:

- **Typography**: Handwritten Great Vibes title, classical Cinzel and Cormorant Garamond fonts
- **Color Palette**: Rich sepia browns (#2c1810), luxurious gold (#d4af37), warm beiges
- **Ornamentation**: Double borders, fleurons (❦), gilded accents
- **Layout**: Museum-quality presentation with ornate frames

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit 1.28+ |
| **Image Processing** | Pillow (PIL) |
| **Language** | Python 3.8+ |
| **Styling** | Custom CSS + Google Fonts |

---

## 📸 Gallery

<div align="center">

### Original vs Processed

| Before | After |
|--------|-------|
| Classic Mona Lisa | Vintage Renaissance Edition |

*Experience 20+ transformative effects*

</div>

---

## 🎓 Advanced Features

### Image Processing Pipeline

```python
1. Rotation & Zoom        → Spatial transformation
2. Color Mode Selection   → Preset adjustments
3. Enhancement Stack      → Saturation, warmth, sharpness
4. Light Manipulation     → Brightness, contrast, highlights
5. Artistic Filters       → Sfumato, edge definition
6. Aging Effects          → Patina, crackle, fade
7. Final Touches          → Vignette, grain, texture
```

### Color Modes

- **Natural** - Preserves original colors
- **Sepia** - Classic antique photography
- **Cool Tone** - Blue-shifted palette
- **Warm Tone** - Enhanced golden hues
- **Monochrome** - Timeless black & white

---

## 🎭 Customization

### Creating Custom Presets

Modify `app.py` to add your own presets:

```python
# Add to Color Grading section
custom_presets = {
    "Vintage Gold": {"warmth": 1.3, "sepia": 0.4},
    "Museum Neutral": {"saturation": 0.7, "fade": 0.15}
}
```

### Adjusting Frame Styles

Edit frame configurations in the sidebar:

```python
frame_styles = {
    "Your Style": {"border": 5, "color": "#custom"}
}
```

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Additional frame styles
- New color grading presets
- Performance optimizations
- Mobile responsiveness
- Batch processing features

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Leonardo da Vinci** - For the timeless masterpiece
- **Musée du Louvre** - Source of the restored image
- **Streamlit Community** - Excellent framework support
- **Renaissance Art** - Endless design inspiration

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sophisticated-palette/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sophisticated-palette/discussions)
- **Email**: your.email@example.com

---

<div align="center">

### ⚜️ *"Art is never finished, only abandoned"* ⚜️
*— Leonardo da Vinci*

---

Made with 🎨 and passion for Renaissance art

**[⬆ Back to Top](#-sophisticated-palette)**

</div>

# AI Image Processing Toolkit for Content Creators

A professional suite of Python scripts designed for advanced image manipulation using state-of-the-art Neural Networks.

## Features

1. **AI Upscaling (4K & Beyond)**
   - Uses OpenCV's DNN Super Resolution module.
   - Supports EDSR, ESPCN, FSRCNN, and LapSRN models.
   - Designed for upscaling 1080p content to 4K with minimal artifacts.

2. **AI Aspect Ratio Conversion (9:16 to 16:9 Outpainting)**
   - Professional-grade outpainting using Stability AI (SDXL).
   - Generates matching environment for portrait images to fit landscape screens.
   - Ideal for turning Reels/Shorts into cinematic wide-angle shots.

---

## Installation

1. Install Python (3.10+ recommended).
2. Install required dependencies:
   ```bash
   pip install opencv-contrib-python requests Pillow
   ```

---

## Usage Guide

### 1. AI Upscaling (Local)
To upscale an image (e.g., from 1080p to 4K):
1. Download pre-trained `.pb` models from [OpenCV Super Resolution Models](https://github.com/Saafke/EDSR_Tensorflow).
2. Place them in a `models/` folder.
3. Run:
   ```bash
   python ai_upscale.py input_image.jpg --scale 4 --model edsr
   ```

### 2. AI Outpainting (9:16 to 16:9)
To expand a portrait image to a full landscape view:
1. Get an API key from [Stability.ai](https://dreamstudio.ai/account).
2. Run:
   ```bash
   python ai_outpaint.py portrait_image.jpg --key YOUR_API_KEY
   ```

---

## Technical Details (Senior Best Practices)
- **DNN Module**: Uses C++ optimized backends for image processing.
- **Aspect Ratio Math**: Automatically calculates padding required for precise 16:9 output.
- **Error Handling**: Comprehensive input validation and logging for production workflows.
- **Scalability**: Designed to be integrated into larger automated rendering pipelines.

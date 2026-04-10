# Advanced Video Automation Toolkit (Task 2)

A collection of professional automation tools for After Effects and AI-driven content creation, designed for senior-level workflows.

## 🚀 Key Features

### 1. Hook Swapper & Variations
- **hook_swapper.jsx**: Automatically creates multiple video variations by swapping different 3-5s "Hooks" with a "Master Body" (CTA).
- **hook_generator.py**: Uses OpenAI/GPT-4o to analyze transcriptions and generate 5 high-converting headlines and visual descriptions for hooks.

### 2. Localization Pipeline
- **localization_pipeline.jsx**: Generates localized video versions based on a CSV configuration.
- **tts_generator.py**: Integrates with ElevenLabs API to generate emotional, multi-lingual voiceovers for the localization pipeline.

### 3. AI Quality Enhancement
- **video_upscale.py**: Uses **Real-ESRGAN** for state-of-the-art frame-by-frame upscaling of low-quality UGC clips to 4K.
- **comfy_bridge.py**: Connects After Effects to a local or remote **ComfyUI** instance for generative AI tasks (outpainting, stylization).

---

## 🏗 Architecture (C4 Model)
For detailed technical documentation and diagrams, see:
- [C4_Architecture.md](C4_Architecture.md) - Core system and container diagrams.
- [C4_ComfyUI.md](C4_ComfyUI.md) - Deep dive into ComfyUI integration.
- [C4_Advanced_AI.md](C4_Advanced_AI.md) - Integration of LLMs, TTS, and Real-ESRGAN.

---

## 🛠 Installation & Setup

### Prerequisites
1. **Adobe After Effects** (Any recent version)
2. **Python 3.10+**
3. **ComfyUI** (Optional, for advanced generative tasks)

### Python Dependencies
```bash
pip install requests openai websocket-client pandas torch basicsr realesrgan opencv-python
```

### Installation
1. Move `.jsx` files to your After Effects `Scripts/ScriptUI Panels` folder.
2. Restart After Effects.
3. Access tools via the `Window` menu.

---

## 📖 Detailed Guides
- [DEPLOYMENT_RU.md](DEPLOYMENT_RU.md) - Инструкция по развертыванию (Russian).
- [DEPLOYMENT_EN.md](DEPLOYMENT_EN.md) - Deployment Guide (English).
- [WORKFLOWS.md](WORKFLOWS.md) - Професійний опис воркфлоу (Ukrainian).

---

## 👨‍💻 Senior Recommendations
- **Dynamic Assets**: Always use absolute paths in CSV configurations to avoid import errors.
- **AI Safety**: Store API keys in environment variables or a secure `.env` file instead of hardcoding them.
- **Scalability**: For large batches, use the `video_upscale.py` script on a dedicated GPU server for better performance.

---
© 2026 Motion Design Automation Suite

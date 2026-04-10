# Motion Design Automation: File Manifest (Task 1 & Task 2)

This document provides a concise description of all scripts and tools developed for both tasks.

---

## 🛠 Task 1: AutoSub & Image Enhancement
*Located in the root directory.*

- **AutoSub_Reels.jsx**: After Effects ScriptUI panel for importing SRT subtitles with word-by-word splitting and "Reels-style" animations.
- **transcribe.py**: Python script using OpenAI Whisper for high-accuracy speech-to-text transcription (outputs .srt).
- **Transcribe_Video.bat**: Windows batch file for easy drag-and-drop video transcription.
- **generate_icon.py**: Utility script to generate a professional .ico file for the batch script.
- **ai_upscale.py**: Image upscaling tool using OpenCV DNN (EDSR/ESPCN models) to enhance photos to 4K.
- **ai_outpaint.py**: Image resizing tool using Stability AI API to expand 9:16 portrait images to 16:9 landscape.

---

## 🚀 Task 2: Video Automation & Advanced AI
*Located in the `task2/` directory.*

- **hook_swapper.jsx**: After Effects script that automatically generates video variations by swapping different 3-5s "Hooks" with a "Master Body".
- **localization_pipeline.jsx**: Automated render pipeline that creates localized versions of a project based on a CSV table (text & voiceover).
- **hook_generator.py**: AI-powered script using GPT-4o to analyze transcriptions and generate 5 viral hook headlines.
- **tts_generator.py**: Professional voiceover generator using ElevenLabs API (supports 29 languages).
- **video_upscale.py**: Advanced video frame upscaler using **Real-ESRGAN** for superior 4K quality.
- **comfy_bridge.py**: API Bridge to connect After Effects with a local/remote ComfyUI instance.
- **comfy_workflow.json**: Sample JSON configuration for ComfyUI API tasks (outpainting/styling).

---
© 2026 Motion Design Automation Suite

# Deployment Guide (Task 2: Hook Swapper & Localization Pipeline)

This guide will help you deploy and configure the tools for automated video production and localization in Adobe After Effects.

## Tool Suite:
1. **hook_swapper.jsx**: Automatic assembly of video variations (hooks + master).
2. **localization_pipeline.jsx**: Automatic localization based on CSV.

---

## Step 1: Script Installation
1. Copy the `.jsx` files from the `task2/` folder into the After Effects scripts folder:
   - **Windows**: `C:\Program Files\Adobe\Adobe After Effects <version>\Support Files\Scripts\ScriptUI Panels`
   - **macOS**: `/Applications/Adobe After Effects <version>/Scripts/ScriptUI Panels`
2. Restart After Effects.

---

## Step 2: Environment Setup (Optional)
To automatically pre-process data (translation, transcription, voiceover), it is recommended to use Python.
1. Install necessary libraries:
   ```bash
   pip install openai-whisper pandas requests
   ```
2. Use **OpenAI Whisper** for transcribing hooks before assembly.
3. Use **GPT-4** to automatically translate texts and generate the localization CSV file.

---

## Step 3: Launch and Usage

### 3.1 Hook Swapper
1. In After Effects, go to `Window > hook_swapper.jsx`.
2. Select the "Master Body" file (main video without a hook).
3. Select the folder containing all hook files (3–5 sec).
4. Click **GENERATE VARIATIONS**. The script will create new compositions and add them to the render queue.

### 3.2 Localization Pipeline
1. Prepare a CSV file with the following columns: `lang`, `headline`, `subtitle`, `cta`, `voiceover_path`.
2. In After Effects, go to `Window > localization_pipeline.jsx`.
3. Select your CSV file.
4. Enter the exact name of your master composition.
5. Click **GENERATE LOCALIZED VERSIONS**.

---

## Senior Developer Recommendations:
- **Layer Names**: Ensure that the names of text layers in AE (headline, subtitle, etc.) exactly match the column headers in the CSV.
- **File Paths**: In the CSV, use absolute paths to voiceover (VO) audio files to avoid import errors.
- **Rendering**: The scripts automatically add compositions to the Render Queue, allowing you to run mass exports with a single click.

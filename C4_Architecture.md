# C4 Architecture: AI Image Toolkit

This document provides a professional architectural overview of the AI Image Toolkit using the C4 model with Mermaid visualizations.

## 1. System Context Diagram (Level 1)
The AI Image Toolkit is a specialized utility suite for content creators (Social Media Managers, Video Editors).

```mermaid
graph TD
    User((Content Creator))
    System[AI Image Toolkit]
    Stability[Stability AI Cloud API]
    OpenCV[OpenCV DNN Models]
    FS[(File System)]

    User -->|Runs Scripts| System
    System -->|Generative Tasks| Stability
    System -->|Deterministic Upscaling| OpenCV
    System -->|Reads/Writes Images| FS
```

- **Users**: Content Creators, Video Editors, Developers.
- **External Systems**:
  - **Stability AI Cloud API**: For high-end generative outpainting (9:16 to 16:9).
  - **OpenCV DNN Models**: Local pre-trained models for super-resolution (4K Upscaling).

---

## 2. Container Diagram (Level 2)
The toolkit consists of two primary processing containers.

```mermaid
graph LR
    subgraph Local_Process [Local Machine]
        US[AI Upscale Script]
        OP[AI Outpaint Script]
    end
    
    FS[(Local Images)] --> US
    FS --> OP
    
    OP -->|Secure API Request| Stability[Stability AI API]
    US -->|Local Inference| OpenCV[OpenCV DNN Engine]
    
    Stability -->|Base64 Artifacts| OP
    OpenCV -->|Processed Image| US
    
    US -->|Saves 4K| FS
    OP -->|Saves 16:9| FS
```

- **AI Upscale Container (Local)**:
  - Language: Python
  - Library: OpenCV (DNN Module)
  - Responsibility: Local high-speed super-resolution processing for images.
- **AI Outpaint Container (Cloud-Hybrid)**:
  - Language: Python
  - Library: Requests, PIL
  - Responsibility: Secure API communication with Stability AI for generative outpainting.

---

## 3. Component Diagram (Level 3)
Internal components of each processing container.

### AI Upscale Components:
```mermaid
graph TD
    CLI[CLI Handler]
    ML[Model Loader]
    DE[DNN Engine]
    IP[Image Processor]

    CLI -->|Params| ML
    CLI -->|Path| IP
    ML -->|Model Config| DE
    IP -->|Input Tensor| DE
    DE -->|Output Tensor| IP
```

1. **Model Loader**: Validates and loads `.pb` model files from the `models/` directory.
2. **DNN Engine**: Performs the actual neural network inference for upscaling.
3. **Image Processor**: Handles reading/writing images and color space conversions.

### AI Outpaint Components:
```mermaid
graph TD
    CLI_OP[CLI Handler]
    DC[Dimension Calculator]
    AC[API Client]
    AP[Artifact Processor]

    CLI_OP -->|Input Size| DC
    DC -->|Padding Data| AC
    CLI_OP -->|API Key| AC
    AC -->|API Call| Stability[Stability AI]
    Stability -->|JSON Response| AP
```

1. **Dimension Calculator**: Computes target 16:9 padding from 9:16 input.
2. **API Client**: Handles authentication and multipart/form-data requests.
3. **Artifact Processor**: Decodes Base64 response artifacts and saves output.

---

## 4. Code Diagram (Level 4)
High-level code structure and flow.

- **Main Entry Point**: `ai_upscale.py` / `ai_outpaint.py`
- **Configuration**: `argparse` for CLI flexibility.
- **Core Logic**:
  - `upscale_image(input, output, scale, model)`: Core function for local SR.
  - `outpaint_image(input, output, api_key)`: Core function for cloud outpainting.

---

## Technical Rationale (Senior Decisions)
- **Decoupled Architecture**: Each processing task is a separate script to allow independent scaling and deployment.
- **Hybrid Approach**: Local execution for deterministic tasks (upscaling) and cloud execution for complex generative tasks (outpainting) to ensure high-quality results without requiring massive local GPUs.
- **Standardized I/O**: Both scripts follow consistent CLI argument patterns for easy automation in build pipelines.

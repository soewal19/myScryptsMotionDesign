# C4 Architecture: ComfyUI Integration Bridge

This document provides a detailed architectural overview of the integration between **After Effects** and **ComfyUI** using the C4 model.

## 1. System Context Diagram (Level 1)
The ComfyUI Bridge acts as a middleware that enables professional video editors to use state-of-the-art generative AI within their AE environment.

```mermaid
graph TD
    User((Video Editor))
    AE[Adobe After Effects]
    Bridge[ComfyUI Bridge Script]
    Comfy[ComfyUI Server]
    FS[(Local Storage)]

    User -->|Initiates Task| AE
    AE -->|Exports Frame| FS
    AE -->|Triggers| Bridge
    Bridge -->|Reads Frame| FS
    Bridge -->|API Request| Comfy
    Comfy -->|Processing| Comfy
    Comfy -->|Saves Result| FS
    Bridge -->|Notifies| AE
    AE -->|Imports Result| FS
```

---

## 2. Container Diagram (Level 2)
Detailed look at the technical containers involved in the bridge.

```mermaid
graph LR
    subgraph AE_Environment [After Effects]
        JSX[AE Script JSX]
    end

    subgraph Python_Runtime [Python Bridge]
        BridgePy[comfy_bridge.py]
        JSON[workflow.json]
    end

    subgraph AI_Backend [ComfyUI Server]
        API[WebSocket/HTTP API]
        Nodes[Custom Node Graph]
    end

    JSX -->|Shell Execute| BridgePy
    BridgePy -->|Loads| JSON
    BridgePy -->|Connects| API
    API -->|Executes| Nodes
    Nodes -->|Returns Progress| API
    API -->|Sends Result| BridgePy
```

---

## 3. Component Diagram (Level 3)
Internal logic of the `comfy_bridge.py` script.

```mermaid
graph TD
    Entry[CLI Entry Point]
    WS[WebSocket Client]
    Prompt[Prompt Manager]
    Assets[Asset Handler]
    History[Execution Tracker]

    Entry --> Prompt
    Prompt -->|Builds JSON| WS
    WS -->|Sends Prompt| Comfy((ComfyUI))
    Comfy -->|Events| History
    History -->|Completion| Assets
    Assets -->|Retrieve Image| Comfy
    Assets -->|Save to Disk| Done[Success]
```

1. **Prompt Manager**: Injects dynamic values (input paths, seeds, prompts) into the static `workflow.json`.
2. **WebSocket Client**: Maintains a persistent connection for real-time progress tracking.
3. **Execution Tracker**: Monitors the ComfyUI history to detect when a specific task is finished.
4. **Asset Handler**: Handles the binary transfer of images between the server and the local filesystem.

---

## 4. Technical Rationale
- **Decoupling**: By using a standalone Python bridge, we avoid blocking the After Effects UI thread during heavy AI generation.
- **Workflow Flexibility**: The bridge is "workflow-agnostic" — you can swap `comfy_workflow.json` for any other AI task (e.g., face swap, stylization) without changing the Python code.
- **Scalability**: The `SERVER_ADDRESS` can be pointed to a remote GPU server or a local machine.

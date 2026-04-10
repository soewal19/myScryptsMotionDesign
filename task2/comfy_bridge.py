import websocket # pip install websocket-client
import uuid
import json
import urllib.request
import urllib.parse
import os
import argparse

# --- CONFIGURATION ---
SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def process_comfy_task(workflow_json_path, input_image_path, output_path):
    """
    Sends a workflow to ComfyUI, replaces input image, and saves output.
    """
    print(f"[*] Loading workflow: {workflow_json_path}")
    with open(workflow_json_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # --- WORKFLOW CUSTOMIZATION ---
    # In a real API workflow, you find the nodes by their title or class
    # Example: Find the LoadImage node and set the path
    for node_id in workflow:
        node = workflow[node_id]
        if node["_meta"]["title"] == "Load Image":
            node["inputs"]["image"] = input_image_path
            print(f"[*] Set input image: {input_image_path}")
    
    # --- EXECUTION ---
    print("[*] Sending prompt to ComfyUI...")
    ws = websocket.WebSocket()
    ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")
    
    prompt_res = queue_prompt(workflow)
    prompt_id = prompt_res['prompt_id']
    print(f"[*] Prompt ID: {prompt_id}")

    # Wait for completion (simple polling for this example)
    print("[*] Waiting for ComfyUI to finish...")
    while True:
        history = get_history(prompt_id)
        if prompt_id in history:
            print("[+] Processing complete!")
            break
    
    # --- RETRIEVE RESULTS ---
    output_node_id = None
    for node_id in workflow:
        if workflow[node_id]["_meta"]["title"] == "Save Image":
            output_node_id = node_id
            break
            
    if output_node_id:
        output_data = history[prompt_id]['outputs'][output_node_id]['images'][0]
        image_bytes = get_image(output_data['filename'], output_data['subfolder'], output_data['type'])
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"[+] Output saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ComfyUI Bridge for After Effects")
    parser.add_argument("--workflow", required=True, help="Path to ComfyUI API JSON workflow")
    parser.add_argument("--input", required=True, help="Path to input image/frame")
    parser.add_argument("--output", required=True, help="Path to save processed result")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.workflow):
        print(f"[!] Error: Workflow file not found: {args.workflow}")
    else:
        try:
            process_comfy_task(args.workflow, args.input, args.output)
        except Exception as e:
            print(f"[!] Error connecting to ComfyUI: {e}")
            print("[!] Make sure ComfyUI is running with --enable-cors-header")

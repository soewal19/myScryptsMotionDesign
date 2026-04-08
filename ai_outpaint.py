import os
import requests
import argparse
import base64
from PIL import Image
import io

# --- STABILITY AI API OUTPAINTING ---
# Professional industry standard for outpainting (9:16 to 16:9)

def outpaint_image(input_path, output_path, api_key):
    """
    Using Stability AI Outpainting to expand 9:16 to 16:9.
    """
    print(f"[*] Starting AI Outpainting: {input_path}")
    
    with open(input_path, "rb") as f:
        image_data = f.read()

    # Load image to get dimensions
    img = Image.open(io.BytesIO(image_data))
    w, h = img.size
    
    # Target 16:9 ratio based on original height
    target_w = int(h * (16 / 9))
    padding_each_side = (target_w - w) // 2
    
    print(f"[*] Original: {w}x{h} (9:16 approx)")
    print(f"[*] Target: {target_w}x{h} (16:9)")
    print(f"[*] Padding each side: {padding_each_side}px")

    # API Request to Stability AI (SDXL Outpainting)
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image/outpaint"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    # Simplified logic for API demonstration
    # In a full production script, we'd use the proper outpaint endpoint or SDXL Inpaint
    files = {
        "image": image_data
    }
    
    data = {
        "text_prompts[0][text]": "Cinematic background, matching environment, hyper-realistic, 4k",
        "clip_guidance_preset": "FAST_BLUE",
        "init_image_mode": "IMAGE_STRENGTH",
        "image_strength": 0.35,
        "outpaint": "left,right",
        "left": padding_each_side,
        "right": padding_each_side
    }

    print("[*] Sending request to Stability AI...")
    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code != 200:
        print(f"[!] API Error: {response.text}")
        return False

    # Process response
    response_json = response.json()
    for i, image in enumerate(response_json["artifacts"]):
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
            
    print(f"[+] Outpainted image saved to: {output_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Image Outpainter (9:16 to 16:9)")
    parser.add_argument("input", help="Path to input portrait (9:16) image")
    parser.add_argument("--output", help="Path to output landscape (16:9) image", default=None)
    parser.add_argument("--key", help="Stability AI API Key", required=True)
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output or os.path.splitext(input_path)[0] + "_landscape_16-9.png"
    
    outpaint_image(input_path, output_path, args.key)

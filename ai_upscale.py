import os
import sys
import argparse
import cv2
from cv2 import dnn_superres

def upscale_image(input_path, output_path, scale=4, model_type="edsr"):
    """
    Upscale image using OpenCV's DNN Super Resolution module.
    Supported models: edsr, espcn, fsrcnn, lapsrn
    """
    print(f"[*] Initializing {model_type.upper()} model for {scale}x upscaling...")
    
    sr = dnn_superres.DnnSuperResImpl_create()
    
    # Path to pre-trained models (assuming they are in a 'models' folder or downloadable)
    # For a production script, we would typically handle model downloading
    model_path = os.path.join(os.path.dirname(__file__), "models", f"{model_type.lower()}_x{scale}.pb")
    
    if not os.path.exists(model_path):
        print(f"[!] Model file not found at {model_path}")
        print(f"[!] Please download the {model_type.upper()} x{scale} model (.pb) from OpenCV's repository.")
        print("    Example: https://github.com/Saafke/EDSR_Tensorflow")
        return False

    sr.readModel(model_path)
    sr.setModel(model_type.lower(), scale)
    
    print(f"[*] Reading image: {input_path}")
    img = cv2.imread(input_path)
    if img is None:
        print("[!] Error: Could not read image.")
        return False

    print("[*] Processing... (this may take a while for 4K output)")
    result = sr.upsample(img)
    
    print(f"[*] Saving upscaled image to: {output_path}")
    cv2.imwrite(output_path, result)
    print("[+] Done!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Image Upscaler to 4K")
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("--output", help="Path to output image", default=None)
    parser.add_argument("--scale", type=int, choices=[2, 3, 4], default=4, help="Upscale factor (2, 3, 4)")
    parser.add_argument("--model", choices=["edsr", "espcn", "fsrcnn", "lapsrn"], default="edsr", help="Model type")
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output or os.path.splitext(input_path)[0] + f"_upscaled_{args.scale}x.jpg"
    
    upscale_image(input_path, output_path, args.scale, args.model)

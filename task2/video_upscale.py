import os
import argparse
import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

def upscale_video_frames(input_folder, output_folder, model_path, scale=4):
    """
    Advanced Video/Frame Upscaling using Real-ESRGAN.
    Ideal for enhancing low-quality UGC clips to 4K.
    """
    print(f"[*] Initializing Real-ESRGAN (x{scale})...")
    
    # Check for CUDA (GPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[*] Running on device: {device}")
    
    # Load Real-ESRGAN Model
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    upsampler = RealESRGANer(
        scale=scale,
        model_path=model_path,
        model=model,
        tile=400,
        tile_pad=10,
        pre_pad=0,
        half=True if device == 'cuda' else False,
        device=device
    )

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    print(f"[*] Found {len(files)} frames to upscale.")

    for i, filename in enumerate(files):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        
        print(f"[*] Processing frame {i+1}/{len(files)}: {filename}...")
        output, _ = upsampler.enhance(img, outscale=scale)
        
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, output)
        
    print(f"[+] Upscaling complete! Frames saved to: {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-ESRGAN Video Frame Upscaler (4K)")
    parser.add_argument("--input", required=True, help="Folder containing video frames")
    parser.add_argument("--output", required=True, help="Folder to save upscaled frames")
    parser.add_argument("--model", required=True, help="Path to Real-ESRGAN .pth model")
    parser.add_argument("--scale", type=int, default=4, help="Upscale factor (e.g., 4)")
    
    args = parser.parse_args()
    upscale_video_frames(args.input, args.output, args.model, args.scale)

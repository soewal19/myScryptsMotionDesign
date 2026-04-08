from PIL import Image, ImageDraw, ImageFont
import os

def generate_autosub_icon():
    # Settings
    size = (256, 256)
    bg_color = (40, 20, 80) # Deep AE Purple
    accent_color = (255, 200, 0) # Reels Yellow
    text_color = (255, 255, 255)
    
    # Create image
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded background
    padding = 20
    draw.rounded_rectangle(
        [padding, padding, size[0]-padding, size[1]-padding], 
        radius=40, 
        fill=bg_color, 
        outline=accent_color, 
        width=8
    )
    
    # Try to draw text
    try:
        # Load a standard Windows font
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        if not os.path.exists(font_path):
            font_path = "arial.ttf"
            
        font = ImageFont.truetype(font_path, 100)
        
        # Center text "SUB"
        text = "SUB"
        w, h = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else draw.textbbox((0, 0), text, font=font)[2:]
        draw.text(((size[0]-w)/2, (size[1]-h)/2 - 10), text, fill=text_color, font=font)
        
        # Draw small "CC" in corner
        small_font = ImageFont.truetype(font_path, 40)
        draw.text((size[0]-80, size[1]-80), "CC", fill=accent_color, font=small_font)
        
    except Exception as e:
        print(f"Font error: {e}. Drawing simple shape instead.")
        draw.rectangle([80, 100, 176, 156], fill=text_color)
        
    # Save as ICO
    icon_path = os.path.join(os.path.dirname(__file__), "autosub.ico")
    img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    print(f"Icon saved to: {icon_path}")

if __name__ == "__main__":
    try:
        generate_autosub_icon()
    except ImportError:
        print("Pillow library not found. Install it with: pip install Pillow")

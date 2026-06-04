from PIL import Image
import os

media_dir = "/Users/simran/.gemini/antigravity-ide/brain/7440bd93-b981-4fcc-8768-153bbbfb328b/.tempmediaStorage"
files = [f for f in os.listdir(media_dir) if f.startswith("media_") and f.endswith(".png")]

for f in sorted(files):
    path = os.path.join(media_dir, f)
    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            w, h = img.size
            
            # Check the top 80 pixels.
            # Let's count how many pixels are sky blue vs browser gray.
            gray_pixels = 0
            sky_pixels = 0
            for y in range(0, min(80, h)):
                for x in range(0, w, 10):
                    r, g, b = img.getpixel((x, y))
                    # Browser tab/toolbar gray is typically around (240, 240, 240) or (242, 243, 245) or (147, 151, 159)
                    if abs(r - g) < 10 and abs(g - b) < 10 and r > 120:
                        gray_pixels += 1
                    # Sky blue is typically R=~90-130, G=~150-180, B=~220-250
                    if 80 < r < 160 and 130 < g < 200 and 200 < b < 255:
                        sky_pixels += 1
                        
            total_checked = w // 10 * min(80, h)
            gray_pct = (gray_pixels / total_checked) * 100
            sky_pct = (sky_pixels / total_checked) * 100
            
            # If sky percentage is high (>50%) and gray is low, this is a sky image!
            if sky_pct > 30:
                print(f"MATCH FOUND: {f} is a sky image!")
                print(f"  Dimensions: {w}x{h}")
                print(f"  Sky pixel % in top 80px: {sky_pct:.1f}%")
                print(f"  Gray pixel % in top 80px: {gray_pct:.1f}%")
                print("-" * 50)
            else:
                # Print stats for other images for debugging
                if sky_pct > 5 or gray_pct < 20:
                    print(f"File: {f}, Size: {w}x{h}, Sky%: {sky_pct:.1f}%, Gray%: {gray_pct:.1f}%")
                    
    except Exception as e:
        pass

from PIL import Image, ImageDraw, ImageFont
import os

BASE = r"C:\Users\juand\OneDrive\Desktop\Workshido"
SIZE = 256

img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

draw.rounded_rectangle([0, 0, SIZE-1, SIZE-1], radius=46, fill=(4, 44, 83))
draw.rectangle([0, SIZE-68, SIZE-1, SIZE-1], fill=(26, 95, 160))
draw.rectangle([0, SIZE-42, SIZE-1, SIZE-1], fill=(55, 138, 221))

try:
    fw = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 148)
    fs = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 96)
except:
    fw = fs = ImageFont.load_default()

draw.text((14, 44), "W", font=fw, fill=(255, 255, 255))
draw.text((162, 24), "S", font=fs, fill=(133, 183, 235))

# PNG sizes
img.save(os.path.join(BASE, "apple-touch-icon.png"))
img.resize((192, 192), Image.LANCZOS).save(os.path.join(BASE, "favicon-192.png"))
img.resize((32, 32),   Image.LANCZOS).save(os.path.join(BASE, "favicon-32x32.png"))
img.resize((16, 16),   Image.LANCZOS).save(os.path.join(BASE, "favicon-16x16.png"))

# favicon.ico (contiene 16, 32 y 48px — lo que Google prefiere)
ico_path = os.path.join(BASE, "favicon.ico")
img.resize((48, 48), Image.LANCZOS).save(
    ico_path,
    format='ICO',
    sizes=[(16,16), (32,32), (48,48)]
)

print("Todos los favicons generados, incluido favicon.ico")

#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFilter

assets_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/02_assets"
target_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/04_hyperframes/assets"
os.makedirs(target_dir, exist_ok=True)

# 1. Copy existing high-res transparent runners
for r_name in ["beat07_sprinter-blocks.png", "beat07_marathoner.png", "beat09_lone-runner.png"]:
    src = f"{assets_dir}/{r_name}"
    dst = f"{target_dir}/{r_name}"
    img = Image.open(src)
    img.save(dst)
    print(f"Copied {r_name} -> {dst}")

# 2. Build Beat 4 Clean Paper Smartphone Cutout (380 x 720)
phone = Image.new("RGBA", (400, 740), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(phone)
# White torn border around phone
p_draw.rounded_rectangle([10, 10, 390, 730], radius=44, fill=(255, 255, 255, 255))
# Dark phone body
p_draw.rounded_rectangle([18, 18, 382, 722], radius=40, fill=(25, 23, 19, 255))
# Dark OLED glass screen
p_draw.rounded_rectangle([32, 54, 368, 686], radius=24, fill=(16, 26, 40, 255))
# Speaker slit & camera dot
p_draw.rounded_rectangle([160, 32, 240, 38], radius=3, fill=(90, 95, 105, 255))
p_draw.ellipse([255, 30, 265, 40], fill=(60, 70, 85, 255))
phone.save(f"{target_dir}/beat04_phone_clean.png")
print("  ✅ Created beat04_phone_clean.png")

# 3. Build 3 Photographic Notification Cards for Beat 4
# Notification 1: Promotion
notif1 = Image.new("RGBA", (440, 130), (0, 0, 0, 0))
n1_draw = ImageDraw.Draw(notif1)
n1_draw.rectangle([6, 6, 434, 124], fill=(255, 255, 255, 255))
n1_draw.rectangle([12, 12, 428, 118], fill=(244, 237, 222, 255), outline=(25, 23, 19, 255), width=3)
# Icon circle (Coral)
n1_draw.ellipse([24, 26, 88, 90], fill=(228, 87, 46, 255))
# Text lines
n1_draw.rectangle([106, 36, 320, 56], fill=(25, 23, 19, 255))
n1_draw.rectangle([106, 68, 260, 80], fill=(120, 115, 105, 255))
notif1.save(f"{target_dir}/beat04_notif_promotion.png")

# Notification 2: Wedding
notif2 = Image.new("RGBA", (440, 130), (0, 0, 0, 0))
n2_draw = ImageDraw.Draw(notif2)
n2_draw.rectangle([6, 6, 434, 124], fill=(255, 255, 255, 255))
n2_draw.rectangle([12, 12, 428, 118], fill=(244, 237, 222, 255), outline=(25, 23, 19, 255), width=3)
# Icon circle (Yellow)
n2_draw.ellipse([24, 26, 88, 90], fill=(255, 213, 31, 255))
# Text lines
n2_draw.rectangle([106, 36, 340, 56], fill=(25, 23, 19, 255))
n2_draw.rectangle([106, 68, 240, 80], fill=(120, 115, 105, 255))
notif2.save(f"{target_dir}/beat04_notif_wedding.png")

# Notification 3: House
notif3 = Image.new("RGBA", (440, 130), (0, 0, 0, 0))
n3_draw = ImageDraw.Draw(notif3)
n3_draw.rectangle([6, 6, 434, 124], fill=(255, 255, 255, 255))
n3_draw.rectangle([12, 12, 428, 118], fill=(244, 237, 222, 255), outline=(25, 23, 19, 255), width=3)
# Icon circle (Navy)
n3_draw.ellipse([24, 26, 88, 90], fill=(46, 64, 87, 255))
# Text lines
n3_draw.rectangle([106, 36, 300, 56], fill=(25, 23, 19, 255))
n3_draw.rectangle([106, 68, 220, 80], fill=(120, 115, 105, 255))
notif3.save(f"{target_dir}/beat04_notif_house.png")

print("  ✅ Created Beat 4 notification cards")

# 4. Create photographic collage cards for Beat 3 with torn borders
for name, jpg_name in [("card_money", "beat03_money_card.jpg"), ("card_city", "beat03_city_card.jpg"), ("card_handshake", "beat03_handshake_card.jpg")]:
    src_jpg = f"{target_dir}/{jpg_name}"
    raw = Image.open(src_jpg).convert("RGBA")
    rw, rh = raw.size
    # Card canvas with white border
    bw, bh = rw + 36, rh + 36
    card = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card)
    c_draw.rectangle([0, 0, bw, bh], fill=(255, 255, 255, 255))
    c_draw.rectangle([6, 6, bw - 6, bh - 6], outline=(25, 23, 19, 255), width=3)
    card.paste(raw, (18, 18))
    card.save(f"{target_dir}/beat03_{name}.png")
    print(f"  ✅ Created beat03_{name}.png")

print("All revised cutout assets generated successfully!")

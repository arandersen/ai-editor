#!/usr/bin/env python3
import os
import math
from PIL import Image, ImageDraw, ImageFilter

out_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/04_hyperframes/assets"
os.makedirs(out_dir, exist_ok=True)

W, H = 1080, 1920

CREAM = (244, 237, 222)       # #F4EDDE
CREAM_DARK = (232, 223, 200)  # #E8DFC8
NAVY = (46, 64, 87)           # #2E4057
NAVY_DARK = (27, 40, 56)      # #1B2838
CORAL = (228, 87, 46)         # #E4572E
YELLOW = (255, 213, 31)       # #FFD51F
INK = (25, 23, 19)            # #191713
WHITE = (255, 255, 255)
DOT_GRAY = (205, 198, 185)

# Helper: Draw dot grid
def draw_dot_grid(draw, box, step=40, radius=2, color=DOT_GRAY):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, step):
        for y in range(y0, y1, step):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)

# Helper: Draw corner masking tape
def draw_tape(img, pos, angle, w=150, h=44):
    tape = Image.new("RGBA", (w, h), (244, 237, 215, 215))
    # add slight drop shadow
    tape_rot = tape.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(tape_rot, pos, tape_rot)

# Helper: Draw torn paper border
def draw_torn_rect(draw, box, fill_color, border_color=WHITE, border_w=12):
    x0, y0, x1, y1 = box
    # outer border
    draw.rectangle([x0 - border_w, y0 - border_w, x1 + border_w, y1 + border_w], fill=border_color)
    draw.rectangle([x0, y0, x1, y1], fill=fill_color)

# ==========================================
# 1. BEAT 1 CLEAN PLATE: Empty 5-lane perspective track
# ==========================================
print("Generating Beat 1 Clean Background (Empty perspective track)...")
b1 = Image.new("RGBA", (W, H), CREAM)
b1_draw = ImageDraw.Draw(b1)

# Subtle background paper texture / dots in margin
draw_dot_grid(b1_draw, (80, 200, 1000, 1800), step=48, radius=2, color=DOT_GRAY)

# Perspective track lines (5 lanes = 6 lines)
# Vanishing point near (540, 240)
vp_x, vp_y = 540, 220
# Top line width: 440px (from x=320 to 760) at y=520
# Bottom line width: 940px (from x=70 to 1010) at y=1700
top_y = 500
bot_y = 1720
num_lanes = 5

for i in range(num_lanes + 1):
    t_ratio = i / num_lanes
    tx = 340 + t_ratio * 400
    bx = 90 + t_ratio * 900
    # draw lane line
    b1_draw.line([(tx, top_y), (bx, bot_y)], fill=NAVY, width=5)

# Horizontal reference lines / markers
for y_frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
    curr_y = top_y + y_frac * (bot_y - top_y)
    lx = 340 * (1 - y_frac) + 90 * y_frac
    rx = 740 * (1 - y_frac) + 990 * y_frac
    b1_draw.line([(lx, curr_y), (rx, curr_y)], fill=(46, 64, 87, 80), width=2)

# Corner color accents (Vox style)
b1_draw.polygon([(40, 180), (140, 180), (100, 480), (40, 480)], fill=NAVY)
b1_draw.polygon([(940, 80), (1040, 80), (1040, 360), (960, 360)], fill=CORAL)
b1_draw.polygon([(40, 1640), (140, 1640), (140, 1860), (40, 1860)], fill=NAVY)
b1_draw.polygon([(940, 1580), (1040, 1580), (1040, 1860), (880, 1860)], fill=CORAL)

b1.convert("RGB").save(f"{out_dir}/beat01_clean_bg.jpg", quality=95)
print("  ✅ Saved beat01_clean_bg.jpg")

# ==========================================
# 2. BEAT 2 CLEAN PLATE: Blank cream canvas (NO desks, NO caps)
# ==========================================
print("Generating Beat 2 Clean Background (Empty canvas)...")
b2 = Image.new("RGBA", (W, H), CREAM)
b2_draw = ImageDraw.Draw(b2)
draw_dot_grid(b2_draw, (80, 200, 1000, 1800), step=48, radius=2, color=DOT_GRAY)
# Corner accents
b2_draw.polygon([(40, 60), (320, 60), (280, 220), (40, 180)], fill=NAVY)
b2_draw.polygon([(820, 1620), (1040, 1560), (1040, 1860), (760, 1860)], fill=CORAL)
b2.convert("RGB").save(f"{out_dir}/beat02_clean_bg.jpg", quality=95)
print("  ✅ Saved beat02_clean_bg.jpg")

# ==========================================
# 3. BEAT 3 CLEAN PLATE: Blank dotted canvas (NO cards)
# ==========================================
print("Generating Beat 3 Clean Background (Blank dotted table)...")
b3 = Image.new("RGBA", (W, H), CREAM)
b3_draw = ImageDraw.Draw(b3)
draw_dot_grid(b3_draw, (60, 160, 1020, 1820), step=40, radius=2, color=DOT_GRAY)
# Center cutting mat border
b3_draw.rectangle([80, 200, 1000, 1780], outline=CREAM_DARK, width=4)
b3.convert("RGB").save(f"{out_dir}/beat03_clean_bg.jpg", quality=95)
print("  ✅ Saved beat03_clean_bg.jpg")

# ==========================================
# 4. BEAT 4 CLEAN PLATE: Blank navy paper sheet (NO phone, NO notifications)
# ==========================================
print("Generating Beat 4 Clean Background (Empty navy paper sheet)...")
b4 = Image.new("RGBA", (W, H), CREAM)
b4_draw = ImageDraw.Draw(b4)
# Large navy sheet with white torn border
sheet_box = (90, 240, 990, 1720)
draw_torn_rect(b4_draw, sheet_box, fill_color=NAVY_DARK, border_color=WHITE, border_w=14)
# Dot grid inside navy sheet
draw_dot_grid(b4_draw, (110, 260, 970, 1700), step=44, radius=2, color=(50, 75, 105))
b4.convert("RGB").save(f"{out_dir}/beat04_clean_bg.jpg", quality=95)
print("  ✅ Saved beat04_clean_bg.jpg")

# ==========================================
# 5. BEAT 5 CLEAN PLATE: Split track (NO pill people)
# ==========================================
print("Generating Beat 5 Clean Background (Empty split tracks)...")
b5 = Image.new("RGBA", (W, H), CREAM)
b5_draw = ImageDraw.Draw(b5)

# Top Track (box: y from 120 to 920)
draw_torn_rect(b5_draw, (70, 100, 1010, 900), fill_color=CREAM, border_color=WHITE, border_w=10)
# Top track lanes
for i in range(5):
    frac = i / 4.0
    tx = 320 + frac * 320
    bx = 120 + frac * 760
    b5_draw.line([(tx, 140), (bx, 880)], fill=NAVY, width=4)

# Checkered finish flag in top track (right rail)
flag_x, flag_y = 660, 260
b5_draw.line([(flag_x + 160, flag_y - 20), (flag_x + 160, flag_y + 190)], fill=INK, width=8)
# flag checkerboard (4x3 squares)
sq = 36
for r in range(3):
    for c in range(4):
        fcol = INK if (r + c) % 2 == 0 else WHITE
        b5_draw.rectangle([flag_x + c * sq, flag_y + r * sq, flag_x + (c+1) * sq, flag_y + (r+1) * sq], fill=fcol)

# Dashed dividing line across the exact center
dash_y = 960
for x in range(40, 1040, 40):
    b5_draw.line([(x, dash_y), (x + 22, dash_y)], fill=INK, width=6)

# Bottom Track (box: y from 1020 to 1820)
draw_torn_rect(b5_draw, (70, 1020, 1010, 1820), fill_color=CREAM, border_color=WHITE, border_w=10)
# Bottom track lanes (drawn in coral)
for i in range(5):
    frac = i / 4.0
    tx = 440 + frac * 200
    bx = 100 + frac * 880
    b5_draw.line([(tx, 1060), (bx, 1800)], fill=CORAL, width=4)

b5.convert("RGB").save(f"{out_dir}/beat05_clean_bg.jpg", quality=95)
print("  ✅ Saved beat05_clean_bg.jpg")

print("All 5 clean background plates created successfully!")

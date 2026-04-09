#!/usr/bin/env python3
"""
Crimson Empire - Game Territory Icons Generator
Generates 8 luminous dark fantasy territory icons at 1024x1024
"""

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import math
import random

# Set random seed for consistency
random.seed(42)

SIZE = 1024
CENTER = SIZE // 2
OUTPUT_DIR = "/root/.openclaw/workspace/game_public/icons_new/"

def create_gradient_background(colors, direction='vertical'):
    """Create a gradient background with deep blue/purple tones"""
    base = Image.new('RGB', (SIZE, SIZE), colors[0])
    draw = ImageDraw.Draw(base)
    
    for i in range(SIZE):
        if direction == 'vertical':
            ratio = i / SIZE
        else:
            ratio = 1 - (i / SIZE)
        
        # Interpolate between colors
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        
        draw.line([(0, i), (SIZE, i)], fill=(r, g, b))
    
    return base

def draw_golden_frame(draw, thickness=25):
    """Draw a golden/silver circular frame"""
    # Outer glow
    for i in range(thickness + 10):
        alpha = int(50 * (1 - i / (thickness + 10)))
        radius = SIZE // 2 - thickness // 2 + i
        if radius > 0:
            draw.ellipse([
                CENTER - radius, CENTER - radius,
                CENTER + radius, CENTER + radius
            ], outline=(255, 215, 0, alpha), width=2)
    
    # Main golden ring
    for i in range(thickness):
        radius = SIZE // 2 - thickness // 2 + i
        # Gold gradient effect
        brightness = 200 + int(55 * math.sin(i / thickness * math.pi))
        draw.ellipse([
            CENTER - radius, CENTER - radius,
            CENTER + radius, CENTER + radius
        ], outline=(255, brightness, 0), width=1)
    
    # Inner highlight
    draw.ellipse([
        CENTER - (SIZE // 2 - thickness // 2), CENTER - (SIZE // 2 - thickness // 2),
        CENTER + (SIZE // 2 - thickness // 2), CENTER + (SIZE // 2 - thickness // 2)
    ], outline=(255, 255, 200), width=1)

def draw_border_outpost():
    """Border Outpost - Golden watchtower with red flags"""
    # Deep blue to purple gradient
    img = create_gradient_background([(30, 40, 80), (60, 40, 90)])
    draw = ImageDraw.Draw(img)
    
    # Ground base
    draw.polygon([
        (SIZE * 0.2, SIZE * 0.85),
        (SIZE * 0.8, SIZE * 0.85),
        (SIZE * 0.9, SIZE * 0.95),
        (SIZE * 0.1, SIZE * 0.95)
    ], fill=(80, 70, 60))
    
    # Main tower structure (golden)
    tower_base_width = SIZE * 0.15
    tower_height = SIZE * 0.45
    tower_bottom_y = SIZE * 0.75
    
    # Tower body
    draw.polygon([
        (CENTER - tower_base_width, tower_bottom_y),
        (CENTER + tower_base_width, tower_bottom_y),
        (CENTER + tower_base_width * 0.8, tower_bottom_y - tower_height),
        (CENTER - tower_base_width * 0.8, tower_bottom_y - tower_height)
    ], fill=(218, 165, 32), outline=(184, 134, 11), width=3)
    
    # Tower top platform
    platform_y = tower_bottom_y - tower_height
    draw.rectangle([
        CENTER - tower_base_width * 1.2, platform_y - SIZE * 0.05,
        CENTER + tower_base_width * 1.2, platform_y + SIZE * 0.05
    ], fill=(200, 150, 30), outline=(150, 100, 10), width=2)
    
    # Watchtower roof (pointed)
    roof_height = SIZE * 0.15
    draw.polygon([
        (CENTER - tower_base_width * 1.3, platform_y - SIZE * 0.05),
        (CENTER + tower_base_width * 1.3, platform_y - SIZE * 0.05),
        (CENTER, platform_y - SIZE * 0.05 - roof_height)
    ], fill=(180, 140, 20), outline=(130, 90, 10), width=2)
    
    # Red flag on pole
    pole_top = (CENTER, platform_y - SIZE * 0.05 - roof_height)
    flag_pole_height = SIZE * 0.12
    
    # Pole
    draw.line([
        pole_top,
        (pole_top[0], pole_top[1] - flag_pole_height)
    ], fill=(150, 150, 150), width=4)
    
    # Waving red flag
    flag_base = (pole_top[0], pole_top[1] - flag_pole_height * 0.7)
    draw.polygon([
        flag_base,
        (flag_base[0] + SIZE * 0.12, flag_base[1] - SIZE * 0.03),
        (flag_base[0] + SIZE * 0.12, flag_base[1] + SIZE * 0.05),
        (flag_base[0], flag_base[1] + SIZE * 0.02)
    ], fill=(220, 40, 40), outline=(180, 20, 20), width=2)
    
    # Flag details (golden emblem)
    draw.ellipse([
        flag_base[0] + SIZE * 0.06 - SIZE * 0.015, flag_base[1] - SIZE * 0.015,
        flag_base[0] + SIZE * 0.06 + SIZE * 0.015, flag_base[1] + SIZE * 0.015
    ], fill=(255, 215, 0))
    
    # Windows (glowing)
    window_y = tower_bottom_y - tower_height * 0.6
    for offset in [-tower_base_width * 0.3, tower_base_width * 0.3]:
        draw.ellipse([
            CENTER + offset - SIZE * 0.02, window_y - SIZE * 0.03,
            CENTER + offset + SIZE * 0.02, window_y + SIZE * 0.03
        ], fill=(255, 200, 100))
    
    # Add glow effect to windows
    for offset in [-tower_base_width * 0.3, tower_base_width * 0.3]:
        for r in range(3, 8):
            draw.ellipse([
                CENTER + offset - SIZE * 0.02 - r, window_y - SIZE * 0.03 - r,
                CENTER + offset + SIZE * 0.02 + r, window_y + SIZE * 0.03 + r
            ], outline=(255, 150, 50, 100), width=1)
    
    # Crenellations on tower
    cren_y = tower_bottom_y - tower_height * 0.15
    for i in range(5):
        cx = CENTER - tower_base_width * 0.8 + (tower_base_width * 1.6 / 4) * i
        draw.rectangle([
            cx - SIZE * 0.015, cren_y - SIZE * 0.04,
            cx + SIZE * 0.015, cren_y
        ], fill=(200, 150, 30))
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}border_outpost.png", "PNG")
    print("✓ border_outpost.png created")

def draw_bandit_camp():
    """Bandit Camp - Brown tents, campfire, camp elements"""
    # Warm orange to deep red gradient
    img = create_gradient_background([(80, 50, 40), (120, 60, 50)])
    draw = ImageDraw.Draw(img)
    
    # Ground (dirt)
    draw.ellipse([
        SIZE * 0.1, SIZE * 0.75, SIZE * 0.9, SIZE * 0.95
    ], fill=(101, 67, 33), outline=(80, 50, 30), width=3)
    
    # Main tent (large, brown)
    tent_base_y = SIZE * 0.7
    tent_width = SIZE * 0.25
    tent_height = SIZE * 0.25
    
    # Tent poles
    draw.line([
        (CENTER - tent_width * 0.6, tent_base_y),
        (CENTER - tent_width * 0.5, tent_base_y - tent_height * 0.3)
    ], fill=(139, 90, 43), width=5)
    draw.line([
        (CENTER + tent_width * 0.6, tent_base_y),
        (CENTER + tent_width * 0.5, tent_base_y - tent_height * 0.3)
    ], fill=(139, 90, 43), width=5)
    
    # Main tent body
    draw.polygon([
        (CENTER - tent_width, tent_base_y),
        (CENTER + tent_width, tent_base_y),
        (CENTER + tent_width * 0.7, tent_base_y - tent_height * 0.5),
        (CENTER, tent_base_y - tent_height),
        (CENTER - tent_width * 0.7, tent_base_y - tent_height * 0.5)
    ], fill=(160, 82, 45), outline=(101, 67, 33), width=3)
    
    # Tent entrance (dark opening)
    draw.polygon([
        (CENTER - SIZE * 0.04, tent_base_y),
        (CENTER + SIZE * 0.04, tent_base_y),
        (CENTER + SIZE * 0.03, tent_base_y - tent_height * 0.4),
        (CENTER - SIZE * 0.03, tent_base_y - tent_height * 0.4)
    ], fill=(60, 40, 30))
    
    # Small tent (left)
    small_tent_x = CENTER - SIZE * 0.2
    small_tent_width = SIZE * 0.12
    small_tent_height = SIZE * 0.12
    draw.polygon([
        (small_tent_x - small_tent_width, tent_base_y + SIZE * 0.05),
        (small_tent_x + small_tent_width, tent_base_y + SIZE * 0.05),
        (small_tent_x, tent_base_y + SIZE * 0.05 - small_tent_height)
    ], fill=(139, 69, 19), outline=(101, 67, 33), width=2)
    
    # Small tent (right)
    small_tent_x = CENTER + SIZE * 0.2
    draw.polygon([
        (small_tent_x - small_tent_width, tent_base_y + SIZE * 0.05),
        (small_tent_x + small_tent_width, tent_base_y + SIZE * 0.05),
        (small_tent_x, tent_base_y + SIZE * 0.05 - small_tent_height)
    ], fill=(139, 69, 19), outline=(101, 67, 33), width=2)
    
    # Campfire (center front)
    fire_y = SIZE * 0.75
    fire_base_width = SIZE * 0.08
    
    # Firewood base
    draw.ellipse([
        CENTER - fire_base_width, fire_y,
        CENTER + fire_base_width, fire_y + SIZE * 0.02
    ], fill=(101, 67, 33))
    
    # Flames (orange/red/yellow gradient)
    flame_height = SIZE * 0.1
    for layer, color in enumerate([(255, 100, 0), (255, 150, 0), (255, 200, 50)]):
        flame_width = fire_base_width * (1 - layer * 0.25)
        draw.polygon([
            (CENTER - flame_width, fire_y),
            (CENTER + flame_width, fire_y),
            (CENTER, fire_y - flame_height + layer * SIZE * 0.015)
        ], fill=color)
    
    # Fire glow
    for r in range(10, 30, 5):
        draw.ellipse([
            CENTER - fire_base_width - r, fire_y - flame_height * 0.5 - r,
            CENTER + fire_base_width + r, fire_y + SIZE * 0.02 + r
        ], outline=(255, 100, 0, 80 - r * 2), width=2)
    
    # Weapons/banners around camp
    # Spear on left
    draw.line([
        (CENTER - SIZE * 0.35, tent_base_y + SIZE * 0.1),
        (CENTER - SIZE * 0.35, tent_base_y - SIZE * 0.15)
    ], fill=(150, 150, 150), width=3)
    draw.polygon([
        (CENTER - SIZE * 0.35, tent_base_y - SIZE * 0.15),
        (CENTER - SIZE * 0.35 + SIZE * 0.02, tent_base_y - SIZE * 0.12),
        (CENTER - SIZE * 0.35 - SIZE * 0.02, tent_base_y - SIZE * 0.12)
    ], fill=(200, 200, 200))
    
    # Banner on right
    banner_x = CENTER + SIZE * 0.35
    draw.line([
        (banner_x, tent_base_y + SIZE * 0.1),
        (banner_x, tent_base_y - SIZE * 0.2)
    ], fill=(139, 90, 43), width=4)
    # Tattered red banner
    draw.polygon([
        (banner_x, tent_base_y - SIZE * 0.2),
        (banner_x + SIZE * 0.1, tent_base_y - SIZE * 0.18),
        (banner_x + SIZE * 0.08, tent_base_y - SIZE * 0.15),
        (banner_x + SIZE * 0.12, tent_base_y - SIZE * 0.12),
        (banner_x, tent_base_y - SIZE * 0.14)
    ], fill=(180, 40, 40), outline=(120, 30, 30), width=2)
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}bandit_camp.png", "PNG")
    print("✓ bandit_camp.png created")

def draw_abandoned_castle():
    """Abandoned Castle - Ruined twin towers, moonlight, desolate feeling"""
    # Night sky gradient (deep blue to purple)
    img = create_gradient_background([(20, 20, 50), (50, 40, 80)])
    draw = ImageDraw.Draw(img)
    
    # Moon (large, pale)
    moon_x = SIZE * 0.75
    moon_y = SIZE * 0.25
    moon_radius = SIZE * 0.08
    
    # Moon glow
    for r in range(int(moon_radius * 2), int(moon_radius), -5):
        draw.ellipse([
            moon_x - r, moon_y - r,
            moon_x + r, moon_y + r
        ], outline=(200, 200, 220, 60), width=3)
    
    # Moon body
    draw.ellipse([
        moon_x - moon_radius, moon_y - moon_radius,
        moon_x + moon_radius, moon_y + moon_radius
    ], fill=(240, 240, 255), outline=(200, 200, 220), width=2)
    
    # Crater details
    draw.ellipse([moon_x - moon_radius * 0.3, moon_y - moon_radius * 0.2,
                  moon_x - moon_radius * 0.15, moon_y - moon_radius * 0.05],
                 fill=(220, 220, 235))
    draw.ellipse([moon_x + moon_radius * 0.2, moon_y + moon_radius * 0.1,
                  moon_x + moon_radius * 0.35, moon_y + moon_radius * 0.25],
                 fill=(220, 220, 235))
    
    # Ground (dark, rocky)
    draw.polygon([
        (0, SIZE * 0.8),
        (SIZE, SIZE * 0.8),
        (SIZE, SIZE),
        (0, SIZE)
    ], fill=(40, 40, 50))
    
    # Left tower (taller, partially ruined)
    left_tower_x = CENTER - SIZE * 0.2
    tower_width = SIZE * 0.12
    tower_height = SIZE * 0.45
    tower_bottom_y = SIZE * 0.82
    
    # Main tower body (crumbling)
    draw.rectangle([
        left_tower_x - tower_width, tower_bottom_y - tower_height,
        left_tower_x + tower_width, tower_bottom_y
    ], fill=(80, 80, 90), outline=(60, 60, 70), width=2)
    
    # Damaged top (jagged)
    draw.polygon([
        (left_tower_x - tower_width, tower_bottom_y - tower_height),
        (left_tower_x - tower_width * 0.8, tower_bottom_y - tower_height - SIZE * 0.05),
        (left_tower_x - tower_width * 0.3, tower_bottom_y - tower_height - SIZE * 0.08),
        (left_tower_x + tower_width * 0.2, tower_bottom_y - tower_height - SIZE * 0.03),
        (left_tower_x + tower_width * 0.6, tower_bottom_y - tower_height - SIZE * 0.06),
        (left_tower_x + tower_width, tower_bottom_y - tower_height)
    ], fill=(70, 70, 80), outline=(50, 50, 60), width=2)
    
    # Cracks in tower
    draw.line([
        (left_tower_x - tower_width * 0.5, tower_bottom_y - tower_height * 0.7),
        (left_tower_x - tower_width * 0.3, tower_bottom_y - tower_height * 0.5)
    ], fill=(50, 50, 60), width=2)
    draw.line([
        (left_tower_x + tower_width * 0.4, tower_bottom_y - tower_height * 0.6),
        (left_tower_x + tower_width * 0.6, tower_bottom_y - tower_height * 0.4)
    ], fill=(50, 50, 60), width=2)
    
    # Right tower (shorter, more ruined)
    right_tower_x = CENTER + SIZE * 0.2
    right_tower_height = SIZE * 0.35
    
    draw.rectangle([
        right_tower_x - tower_width * 0.9, tower_bottom_y - right_tower_height,
        right_tower_x + tower_width * 0.9, tower_bottom_y
    ], fill=(75, 75, 85), outline=(55, 55, 65), width=2)
    
    # Heavily damaged top
    draw.polygon([
        (right_tower_x - tower_width * 0.9, tower_bottom_y - right_tower_height),
        (right_tower_x - tower_width * 0.5, tower_bottom_y - right_tower_height - SIZE * 0.04),
        (right_tower_x + tower_width * 0.3, tower_bottom_y - right_tower_height - SIZE * 0.07),
        (right_tower_x + tower_width * 0.9, tower_bottom_y - right_tower_height)
    ], fill=(65, 65, 75), outline=(45, 45, 55), width=2)
    
    # Connecting wall (broken)
    wall_y = tower_bottom_y - tower_height * 0.6
    draw.rectangle([
        left_tower_x + tower_width, wall_y - SIZE * 0.03,
        right_tower_x - tower_width * 0.9, wall_y + SIZE * 0.03
    ], fill=(70, 70, 80))
    
    # Gap in wall
    draw.rectangle([
        CENTER - SIZE * 0.05, wall_y - SIZE * 0.04,
        CENTER + SIZE * 0.05, wall_y + SIZE * 0.04
    ], fill=(20, 20, 50))
    
    # Broken archway
    draw.arc([
        CENTER - SIZE * 0.06, wall_y - SIZE * 0.08,
        CENTER + SIZE * 0.06, wall_y + SIZE * 0.08
    ], 0, 180, fill=(60, 60, 70), width=4)
    
    # Moonlight beams
    for i in range(5):
        beam_x = moon_x - SIZE * 0.15 + i * SIZE * 0.08
        beam_width = SIZE * 0.03
        draw.polygon([
            (beam_x - beam_width, moon_y + moon_radius),
            (beam_x + beam_width, moon_y + moon_radius),
            (beam_x + beam_width * 2, SIZE),
            (beam_x - beam_width * 2, SIZE)
        ], fill=(180, 180, 200, 30))
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}abandoned_castle.png", "PNG")
    print("✓ abandoned_castle.png created")

def draw_orc_tribe():
    """Orc Tribe - Totem poles, skulls, green energy"""
    # Dark green to purple gradient
    img = create_gradient_background([(30, 50, 40), (60, 40, 70)])
    draw = ImageDraw.Draw(img)
    
    # Ground (dark earth)
    draw.ellipse([
        SIZE * 0.1, SIZE * 0.8, SIZE * 0.9, SIZE * 0.95
    ], fill=(50, 40, 30), outline=(30, 25, 20), width=3)
    
    # Central totem pole (tall, wooden)
    totem_x = CENTER
    totem_width = SIZE * 0.12
    totem_height = SIZE * 0.55
    totem_bottom_y = SIZE * 0.82
    
    # Totem base
    draw.rectangle([
        totem_x - totem_width * 0.8, totem_bottom_y - SIZE * 0.05,
        totem_x + totem_width * 0.8, totem_bottom_y
    ], fill=(101, 67, 33), outline=(60, 40, 20), width=2)
    
    # Main totem pole body
    draw.rectangle([
        totem_x - totem_width, totem_bottom_y - totem_height,
        totem_x + totem_width, totem_bottom_y - SIZE * 0.05
    ], fill=(139, 90, 43), outline=(101, 67, 33), width=3)
    
    # Skull carving (top section)
    skull_y = totem_bottom_y - totem_height * 0.25
    # Skull shape
    draw.ellipse([
        totem_x - totem_width * 0.6, skull_y - SIZE * 0.04,
        totem_x + totem_width * 0.6, skull_y + SIZE * 0.04
    ], fill=(200, 190, 180), outline=(150, 140, 130), width=2)
    
    # Eye sockets (glowing green)
    for offset in [-totem_width * 0.25, totem_width * 0.25]:
        draw.ellipse([
            totem_x + offset - SIZE * 0.015, skull_y - SIZE * 0.015,
            totem_x + offset + SIZE * 0.015, skull_y + SIZE * 0.015
        ], fill=(100, 255, 100))
        # Glow
        draw.ellipse([
            totem_x + offset - SIZE * 0.025, skull_y - SIZE * 0.025,
            totem_x + offset + SIZE * 0.025, skull_y + SIZE * 0.025
        ], outline=(50, 200, 50, 150), width=2)
    
    # Nose cavity
    draw.polygon([
        (totem_x - SIZE * 0.01, skull_y + SIZE * 0.01),
        (totem_x + SIZE * 0.01, skull_y + SIZE * 0.01),
        (totem_x, skull_y + SIZE * 0.03)
    ], fill=(80, 60, 50))
    
    # Teeth
    for i in range(5):
        tooth_x = totem_x - SIZE * 0.035 + i * SIZE * 0.018
        draw.polygon([
            (tooth_x, skull_y + SIZE * 0.035),
            (tooth_x + SIZE * 0.012, skull_y + SIZE * 0.035),
            (tooth_x + SIZE * 0.006, skull_y + SIZE * 0.045)
        ], fill=(220, 210, 200))
    
    # Tribal symbols (middle section)
    symbol_y = totem_bottom_y - totem_height * 0.55
    # Green tribal pattern
    for i in range(3):
        sy = symbol_y + i * SIZE * 0.025
        draw.line([
            (totem_x - totem_width * 0.5, sy),
            (totem_x - totem_width * 0.2, sy + SIZE * 0.02),
            (totem_x + totem_width * 0.2, sy),
            (totem_x + totem_width * 0.5, sy + SIZE * 0.02)
        ], fill=(100, 255, 100), width=3)
    
    # Top spike
    draw.polygon([
        (totem_x - totem_width * 0.3, totem_bottom_y - totem_height),
        (totem_x + totem_width * 0.3, totem_bottom_y - totem_height),
        (totem_x, totem_bottom_y - totem_height - SIZE * 0.1)
    ], fill=(101, 67, 33), outline=(60, 40, 20), width=2)
    
    # Green energy aura around totem
    for r in range(20, 50, 10):
        alpha = 100 - r * 2
        draw.ellipse([
            totem_x - totem_width - r, totem_bottom_y - totem_height * 0.5 - r,
            totem_x + totem_width + r, totem_bottom_y - SIZE * 0.05 + r
        ], outline=(50, 255, 50, alpha), width=2)
    
    # Smaller side totems
    for offset in [-SIZE * 0.25, SIZE * 0.25]:
        side_totem_x = totem_x + offset
        side_height = totem_height * 0.5
        
        draw.rectangle([
            side_totem_x - totem_width * 0.5, totem_bottom_y - side_height,
            side_totem_x + totem_width * 0.5, totem_bottom_y - SIZE * 0.03
        ], fill=(101, 67, 33), outline=(60, 40, 20), width=2)
        
        # Small skull
        side_skull_y = totem_bottom_y - side_height * 0.5
        draw.ellipse([
            side_totem_x - totem_width * 0.3, side_skull_y - SIZE * 0.025,
            side_totem_x + totem_width * 0.3, side_skull_y + SIZE * 0.025
        ], fill=(180, 170, 160), outline=(130, 120, 110), width=2)
        
        # Glowing eyes
        for eoffset in [-totem_width * 0.12, totem_width * 0.12]:
            draw.ellipse([
                side_totem_x + eoffset - SIZE * 0.008, side_skull_y - SIZE * 0.008,
                side_totem_x + eoffset + SIZE * 0.008, side_skull_y + SIZE * 0.008
            ], fill=(80, 220, 80))
    
    # Floating green energy particles
    for _ in range(15):
        px = random.uniform(SIZE * 0.3, SIZE * 0.7)
        py = random.uniform(SIZE * 0.3, SIZE * 0.7)
        pr = random.uniform(3, 8)
        draw.ellipse([
            px - pr, py - pr, px + pr, py + pr
        ], fill=(100, 255, 100, 180))
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}orc_tribe.png", "PNG")
    print("✓ orc_tribe.png created")

def draw_dark_fortress():
    """Dark Fortress - Solid walls, golden window lights"""
    # Deep blue to dark purple gradient
    img = create_gradient_background([(25, 30, 60), (55, 40, 80)])
    draw = ImageDraw.Draw(img)
    
    # Ground (dark stone)
    draw.rectangle([
        0, SIZE * 0.85, SIZE, SIZE
    ], fill=(50, 50, 60))
    
    # Main fortress wall (massive, imposing)
    wall_width = SIZE * 0.7
    wall_height = SIZE * 0.35
    wall_bottom_y = SIZE * 0.85
    
    # Base wall
    draw.rectangle([
        CENTER - wall_width * 0.5, wall_bottom_y - wall_height,
        CENTER + wall_width * 0.5, wall_bottom_y
    ], fill=(60, 60, 70), outline=(40, 40, 50), width=3)
    
    # Stone texture lines
    for i in range(8):
        y = wall_bottom_y - wall_height + i * (wall_height / 8)
        draw.line([
            (CENTER - wall_width * 0.5, y),
            (CENTER + wall_width * 0.5, y)
        ], fill=(50, 50, 60), width=1)
    
    # Vertical stone divisions
    for i in range(12):
        x = CENTER - wall_width * 0.5 + i * (wall_width / 12)
        offset = random.randint(-5, 5)
        draw.line([
            (x, wall_bottom_y - wall_height + offset),
            (x, wall_bottom_y + offset)
        ], fill=(50, 50, 60), width=1)
    
    # Central gate (arched, dark)
    gate_width = SIZE * 0.15
    gate_height = SIZE * 0.25
    draw.polygon([
        (CENTER - gate_width * 0.5, wall_bottom_y),
        (CENTER + gate_width * 0.5, wall_bottom_y),
        (CENTER + gate_width * 0.5, wall_bottom_y - gate_height * 0.7),
        (CENTER, wall_bottom_y - gate_height),
        (CENTER - gate_width * 0.5, wall_bottom_y - gate_height * 0.7)
    ], fill=(30, 30, 40), outline=(40, 40, 50), width=3)
    
    # Portcullis (gate bars)
    for i in range(5):
        bar_x = CENTER - gate_width * 0.35 + i * (gate_width * 0.7 / 4)
        draw.line([
            (bar_x, wall_bottom_y - gate_height * 0.8),
            (bar_x, wall_bottom_y)
        ], fill=(80, 80, 90), width=3)
    
    # Left tower
    left_tower_x = CENTER - wall_width * 0.35
    tower_width = SIZE * 0.12
    tower_height = SIZE * 0.3
    
    draw.rectangle([
        left_tower_x - tower_width * 0.5, wall_bottom_y - wall_height - tower_height,
        left_tower_x + tower_width * 0.5, wall_bottom_y - wall_height
    ], fill=(65, 65, 75), outline=(45, 45, 55), width=2)
    
    # Tower roof (pointed, dark)
    draw.polygon([
        (left_tower_x - tower_width * 0.7, wall_bottom_y - wall_height - tower_height),
        (left_tower_x + tower_width * 0.7, wall_bottom_y - wall_height - tower_height),
        (left_tower_x, wall_bottom_y - wall_height - tower_height - SIZE * 0.1)
    ], fill=(50, 50, 60), outline=(35, 35, 45), width=2)
    
    # Right tower (mirror)
    right_tower_x = CENTER + wall_width * 0.35
    draw.rectangle([
        right_tower_x - tower_width * 0.5, wall_bottom_y - wall_height - tower_height,
        right_tower_x + tower_width * 0.5, wall_bottom_y - wall_height
    ], fill=(65, 65, 75), outline=(45, 45, 55), width=2)
    
    draw.polygon([
        (right_tower_x - tower_width * 0.7, wall_bottom_y - wall_height - tower_height),
        (right_tower_x + tower_width * 0.7, wall_bottom_y - wall_height - tower_height),
        (right_tower_x, wall_bottom_y - wall_height - tower_height - SIZE * 0.1)
    ], fill=(50, 50, 60), outline=(35, 35, 45), width=2)
    
    # Golden window lights (multiple floors)
    window_rows = [
        wall_bottom_y - wall_height * 0.8,
        wall_bottom_y - wall_height * 0.5,
        wall_bottom_y - wall_height * 0.2
    ]
    
    for row_y in window_rows:
        # Left section windows
        for i in range(3):
            wx = CENTER - wall_width * 0.35 + i * SIZE * 0.06
            # Window glow
            draw.ellipse([
                wx - SIZE * 0.015, row_y - SIZE * 0.025,
                wx + SIZE * 0.015, row_y + SIZE * 0.025
            ], fill=(255, 200, 100))
            # Outer glow
            for r in range(3, 8):
                draw.ellipse([
                    wx - SIZE * 0.015 - r, row_y - SIZE * 0.025 - r,
                    wx + SIZE * 0.015 + r, row_y + SIZE * 0.025 + r
                ], outline=(255, 150, 50, 80), width=1)
        
        # Right section windows
        for i in range(3):
            wx = CENTER + wall_width * 0.15 + i * SIZE * 0.06
            draw.ellipse([
                wx - SIZE * 0.015, row_y - SIZE * 0.025,
                wx + SIZE * 0.015, row_y + SIZE * 0.025
            ], fill=(255, 200, 100))
            for r in range(3, 8):
                draw.ellipse([
                    wx - SIZE * 0.015 - r, row_y - SIZE * 0.025 - r,
                    wx + SIZE * 0.015 + r, row_y + SIZE * 0.025 + r
                ], outline=(255, 150, 50, 80), width=1)
    
    # Tower windows (glowing)
    for tower_x in [left_tower_x, right_tower_x]:
        for i in range(2):
            wy = wall_bottom_y - wall_height - tower_height * (0.3 + i * 0.35)
            draw.ellipse([
                tower_x - SIZE * 0.02, wy - SIZE * 0.025,
                tower_x + SIZE * 0.02, wy + SIZE * 0.025
            ], fill=(255, 220, 120))
            for r in range(3, 10):
                draw.ellipse([
                    tower_x - SIZE * 0.02 - r, wy - SIZE * 0.025 - r,
                    tower_x + SIZE * 0.02 + r, wy + SIZE * 0.025 + r
                ], outline=(255, 150, 50, 70), width=1)
    
    # Crenellations along wall top
    for i in range(10):
        cx = CENTER - wall_width * 0.45 + i * (wall_width * 0.9 / 9)
        draw.rectangle([
            cx - SIZE * 0.02, wall_bottom_y - wall_height - SIZE * 0.04,
            cx + SIZE * 0.02, wall_bottom_y - wall_height
        ], fill=(65, 65, 75))
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}dark_fortress.png", "PNG")
    print("✓ dark_fortress.png created")

def draw_dragon_lair():
    """Dragon Lair - Red dragon silhouette, golden horns, flames"""
    # Fiery orange to deep red gradient
    img = create_gradient_background([(80, 30, 20), (120, 40, 30)])
    draw = ImageDraw.Draw(img)
    
    # Cave floor (dark, rocky)
    draw.polygon([
        (0, SIZE * 0.75),
        (SIZE, SIZE * 0.75),
        (SIZE, SIZE),
        (0, SIZE)
    ], fill=(40, 30, 25))
    
    # Dragon silhouette (massive, coiled)
    dragon_center_x = CENTER
    dragon_center_y = SIZE * 0.55
    dragon_scale = SIZE * 0.35
    
    # Body (coiled, serpentine)
    # Main body mass
    for i in range(8):
        angle = i * 0.8
        bx = dragon_center_x + math.cos(angle) * dragon_scale * 0.6
        by = dragon_center_y + math.sin(angle) * dragon_scale * 0.4
        br = dragon_scale * (0.3 - i * 0.025)
        draw.ellipse([
            bx - br, by - br,
            bx + br, by + br
        ], fill=(60, 20, 15))
    
    # Dragon head (prominent, facing forward)
    head_x = dragon_center_x
    head_y = dragon_center_y - dragon_scale * 0.5
    head_width = SIZE * 0.12
    head_height = SIZE * 0.1
    
    # Head shape
    draw.polygon([
        (head_x - head_width * 0.5, head_y + head_height * 0.3),
        (head_x + head_width * 0.5, head_y + head_height * 0.3),
        (head_x + head_width * 0.3, head_y - head_height * 0.5),
        (head_x - head_width * 0.3, head_y - head_height * 0.5)
    ], fill=(50, 15, 10))
    
    # Golden horns (large, curved)
    # Left horn
    horn_points = []
    for i in range(20):
        angle = math.pi * 0.6 + i * 0.08
        hx = head_x - head_width * 0.3 + math.cos(angle) * SIZE * 0.08 * i
        hy = head_y - head_height * 0.3 + math.sin(angle) * SIZE * 0.08 * i
        horn_points.append((hx, hy))
    
    if len(horn_points) > 1:
        draw.line(horn_points, fill=(255, 215, 0), width=6)
        # Horn highlight
        draw.line(horn_points, fill=(255, 255, 200), width=2)
    
    # Right horn
    horn_points = []
    for i in range(20):
        angle = math.pi * 0.4 - i * 0.08
        hx = head_x + head_width * 0.3 + math.cos(angle) * SIZE * 0.08 * i
        hy = head_y - head_height * 0.3 + math.sin(angle) * SIZE * 0.08 * i
        horn_points.append((hx, hy))
    
    if len(horn_points) > 1:
        draw.line(horn_points, fill=(255, 215, 0), width=6)
        draw.line(horn_points, fill=(255, 255, 200), width=2)
    
    # Glowing eyes (intense orange/red)
    for offset in [-head_width * 0.2, head_width * 0.2]:
        eye_x = head_x + offset
        eye_y = head_y - head_height * 0.1
        
        # Eye glow
        for r in range(15, 5, -3):
            draw.ellipse([
                eye_x - r * 0.6, eye_y - r * 0.4,
                eye_x + r * 0.6, eye_y + r * 0.4
            ], outline=(255, 100, 0, 100 - r * 5), width=2)
        
        # Eye core
        draw.ellipse([
            eye_x - SIZE * 0.012, eye_y - SIZE * 0.015,
            eye_x + SIZE * 0.012, eye_y + SIZE * 0.015
        ], fill=(255, 200, 50))
        
        # Pupil (slit)
        draw.rectangle([
            eye_x - SIZE * 0.003, eye_y - SIZE * 0.02,
            eye_x + SIZE * 0.003, eye_y + SIZE * 0.02
        ], fill=(20, 10, 5))
    
    # Flames (surrounding the dragon)
    flame_positions = [
        (CENTER - SIZE * 0.25, SIZE * 0.7),
        (CENTER + SIZE * 0.25, SIZE * 0.7),
        (CENTER, SIZE * 0.8),
        (CENTER - SIZE * 0.15, SIZE * 0.85),
        (CENTER + SIZE * 0.15, SIZE * 0.85)
    ]
    
    for fx, fy in flame_positions:
        # Multiple flame layers
        for layer, (color, size_mult) in enumerate([
            ((255, 50, 0), 1.0),
            ((255, 100, 0), 0.85),
            ((255, 150, 0), 0.7),
            ((255, 200, 50), 0.55)
        ]):
            flame_height = SIZE * 0.08 * size_mult
            flame_width = SIZE * 0.04 * size_mult
            
            # Flame shape
            draw.polygon([
                (fx - flame_width, fy),
                (fx + flame_width, fy),
                (fx + flame_width * 0.5, fy - flame_height * 0.7),
                (fx, fy - flame_height),
                (fx - flame_width * 0.5, fy - flame_height * 0.7)
            ], fill=color)
    
    # Fire glow around entire scene
    for r in range(30, 60, 10):
        draw.ellipse([
            CENTER - dragon_scale - r, SIZE * 0.4 - r,
            CENTER + dragon_scale + r, SIZE * 0.85 + r
        ], outline=(255, 100, 0, 40 - r), width=2)
    
    # Treasure/gold pile (subtle, in foreground)
    draw.ellipse([
        CENTER - SIZE * 0.2, SIZE * 0.82,
        CENTER + SIZE * 0.2, SIZE * 0.88
    ], fill=(180, 150, 50, 100))
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}dragon_lair.png", "PNG")
    print("✓ dragon_lair.png created")

def draw_demon_throne():
    """Demon Throne - Purple throne, red demon symbols"""
    # Deep purple to crimson gradient
    img = create_gradient_background([(50, 20, 60), (90, 30, 50)])
    draw = ImageDraw.Draw(img)
    
    # Throne platform (dark stone)
    draw.polygon([
        (SIZE * 0.2, SIZE * 0.75),
        (SIZE * 0.8, SIZE * 0.75),
        (SIZE * 0.85, SIZE * 0.9),
        (SIZE * 0.15, SIZE * 0.9)
    ], fill=(40, 30, 50), outline=(30, 20, 40), width=3)
    
    # Steps
    for i in range(3):
        step_y = SIZE * 0.75 + i * SIZE * 0.05
        draw.rectangle([
            SIZE * 0.25 - i * SIZE * 0.03, step_y,
            SIZE * 0.75 + i * SIZE * 0.03, step_y + SIZE * 0.03
        ], fill=(45, 35, 55), outline=(30, 20, 40), width=1)
    
    # Main throne structure
    throne_x = CENTER
    throne_y = SIZE * 0.55
    throne_width = SIZE * 0.25
    throne_height = SIZE * 0.35
    
    # Throne base
    draw.polygon([
        (throne_x - throne_width * 0.5, SIZE * 0.75),
        (throne_x + throne_width * 0.5, SIZE * 0.75),
        (throne_x + throne_width * 0.4, SIZE * 0.75 - SIZE * 0.08),
        (throne_x - throne_width * 0.4, SIZE * 0.75 - SIZE * 0.08)
    ], fill=(60, 30, 70), outline=(40, 20, 50), width=2)
    
    # Throne back (tall, ornate)
    draw.polygon([
        (throne_x - throne_width * 0.45, SIZE * 0.75 - SIZE * 0.08),
        (throne_x + throne_width * 0.45, SIZE * 0.75 - SIZE * 0.08),
        (throne_x + throne_width * 0.5, throne_y - throne_height),
        (throne_x, throne_y - throne_height - SIZE * 0.08),
        (throne_x - throne_width * 0.5, throne_y - throne_height)
    ], fill=(70, 35, 80), outline=(50, 25, 60), width=3)
    
    # Throne arms (curved, menacing)
    # Left arm
    draw.polygon([
        (throne_x - throne_width * 0.45, SIZE * 0.75 - SIZE * 0.08),
        (throne_x - throne_width * 0.55, SIZE * 0.75 - SIZE * 0.08),
        (throne_x - throne_width * 0.6, SIZE * 0.65),
        (throne_x - throne_width * 0.5, SIZE * 0.65)
    ], fill=(65, 32, 75), outline=(45, 22, 55), width=2)
    
    # Right arm
    draw.polygon([
        (throne_x + throne_width * 0.45, SIZE * 0.75 - SIZE * 0.08),
        (throne_x + throne_width * 0.55, SIZE * 0.75 - SIZE * 0.08),
        (throne_x + throne_width * 0.6, SIZE * 0.65),
        (throne_x + throne_width * 0.5, SIZE * 0.65)
    ], fill=(65, 32, 75), outline=(45, 22, 55), width=2)
    
    # Seat cushion (dark red)
    draw.ellipse([
        throne_x - throne_width * 0.35, SIZE * 0.75 - SIZE * 0.15,
        throne_x + throne_width * 0.35, SIZE * 0.75 - SIZE * 0.05
    ], fill=(100, 20, 40), outline=(80, 15, 30), width=2)
    
    # Demon symbol (large, glowing red, on throne back)
    symbol_x = CENTER
    symbol_y = throne_y - throne_height * 0.5
    symbol_size = SIZE * 0.08
    
    # Outer circle
    draw.ellipse([
        symbol_x - symbol_size, symbol_y - symbol_size,
        symbol_x + symbol_size, symbol_y + symbol_size
    ], outline=(255, 50, 50), width=3)
    
    # Inner pentagram-like shape
    points = []
    for i in range(5):
        angle = -math.pi / 2 + i * 2 * math.pi / 5
        points.append((
            symbol_x + math.cos(angle) * symbol_size * 0.7,
            symbol_y + math.sin(angle) * symbol_size * 0.7
        ))
    
    # Draw star
    for i in range(5):
        draw.line([
            points[i],
            points[(i + 2) % 5]
        ], fill=(255, 30, 30), width=3)
    
    # Center circle
    draw.ellipse([
        symbol_x - symbol_size * 0.2, symbol_y - symbol_size * 0.2,
        symbol_x + symbol_size * 0.2, symbol_y + symbol_size * 0.2
    ], fill=(255, 20, 20))
    
    # Symbol glow
    for r in range(int(symbol_size * 1.2), int(symbol_size * 1.8), 3):
        draw.ellipse([
            symbol_x - r, symbol_y - r,
            symbol_x + r, symbol_y + r
        ], outline=(255, 50, 50, 80), width=1)
    
    # Smaller demon symbols (floating around)
    for sx, sy in [
        (CENTER - SIZE * 0.2, SIZE * 0.4),
        (CENTER + SIZE * 0.2, SIZE * 0.45),
        (CENTER - SIZE * 0.15, SIZE * 0.35),
        (CENTER + SIZE * 0.15, SIZE * 0.38)
    ]:
        # Small symbol
        ss = SIZE * 0.03
        draw.ellipse([sx - ss, sy - ss, sx + ss, sy + ss], outline=(255, 40, 40, 150), width=2)
        # Inner mark
        draw.line([(sx - ss * 0.5, sy), (sx + ss * 0.5, sy)], fill=(255, 30, 30, 150), width=2)
        draw.line([(sx, sy - ss * 0.5), (sx, sy + ss * 0.5)], fill=(255, 30, 30, 150), width=2)
    
    # Purple energy aura around throne
    for r in range(20, 50, 10):
        alpha = 80 - r
        draw.ellipse([
            CENTER - throne_width * 0.7 - r, SIZE * 0.5 - r,
            CENTER + throne_width * 0.7 + r, SIZE * 0.8 + r
        ], outline=(180, 50, 200, alpha), width=2)
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}demon_throne.png", "PNG")
    print("✓ demon_throne.png created")

def draw_void_temple():
    """Void Temple - Purple temple, energy orbs and beams"""
    # Deep purple to dark blue gradient
    img = create_gradient_background([(40, 20, 70), (70, 30, 90)])
    draw = ImageDraw.Draw(img)
    
    # Temple platform (floating)
    platform_y = SIZE * 0.75
    platform_width = SIZE * 0.7
    
    draw.polygon([
        (CENTER - platform_width * 0.5, platform_y),
        (CENTER + platform_width * 0.5, platform_y),
        (CENTER + platform_width * 0.55, platform_y + SIZE * 0.08),
        (CENTER - platform_width * 0.55, platform_y + SIZE * 0.08)
    ], fill=(50, 30, 80), outline=(35, 20, 60), width=3)
    
    # Main temple structure
    temple_x = CENTER
    temple_y = SIZE * 0.5
    temple_width = SIZE * 0.35
    temple_height = SIZE * 0.35
    
    # Temple base
    draw.rectangle([
        temple_x - temple_width * 0.5, platform_y - SIZE * 0.08,
        temple_x + temple_width * 0.5, platform_y
    ], fill=(60, 35, 90), outline=(40, 25, 70), width=2)
    
    # Temple walls
    draw.rectangle([
        temple_x - temple_width * 0.4, platform_y - SIZE * 0.08 - temple_height * 0.7,
        temple_x + temple_width * 0.4, platform_y - SIZE * 0.08
    ], fill=(70, 40, 100), outline=(50, 30, 80), width=2)
    
    # Temple roof (pointed, mystical)
    draw.polygon([
        (temple_x - temple_width * 0.55, platform_y - SIZE * 0.08 - temple_height * 0.7),
        (temple_x + temple_width * 0.55, platform_y - SIZE * 0.08 - temple_height * 0.7),
        (temple_x, platform_y - SIZE * 0.08 - temple_height * 0.7 - SIZE * 0.12)
    ], fill=(80, 45, 110), outline=(55, 35, 85), width=2)
    
    # Roof spire
    draw.line([
        (temple_x, platform_y - SIZE * 0.08 - temple_height * 0.7 - SIZE * 0.12),
        (temple_x, platform_y - SIZE * 0.08 - temple_height * 0.7 - SIZE * 0.2)
    ], fill=(150, 100, 200), width=4)
    
    # Entrance (dark, mysterious)
    entrance_width = SIZE * 0.12
    entrance_height = SIZE * 0.15
    draw.polygon([
        (temple_x - entrance_width * 0.5, platform_y),
        (temple_x + entrance_width * 0.5, platform_y),
        (temple_x + entrance_width * 0.5, platform_y - entrance_height * 0.8),
        (temple_x, platform_y - entrance_height),
        (temple_x - entrance_width * 0.5, platform_y - entrance_height * 0.8)
    ], fill=(20, 10, 40), outline=(40, 25, 70), width=2)
    
    # Entrance glow (purple energy)
    for r in range(5, 15, 3):
        draw.arc([
            temple_x - entrance_width * 0.4 - r, platform_y - entrance_height - r,
            temple_x + entrance_width * 0.4 + r, platform_y + r
        ], 0, 180, fill=(150, 50, 200, 80 - r * 4), width=2)
    
    # Side pillars
    for offset in [-temple_width * 0.6, temple_width * 0.6]:
        pillar_x = temple_x + offset
        pillar_width = SIZE * 0.05
        pillar_height = SIZE * 0.2
        
        draw.rectangle([
            pillar_x - pillar_width * 0.5, platform_y - SIZE * 0.08 - pillar_height,
            pillar_x + pillar_width * 0.5, platform_y - SIZE * 0.08
        ], fill=(75, 42, 105), outline=(50, 30, 80), width=2)
        
        # Pillar top
        draw.rectangle([
            pillar_x - pillar_width * 0.7, platform_y - SIZE * 0.08 - pillar_height,
            pillar_x + pillar_width * 0.7, platform_y - SIZE * 0.08 - pillar_height + SIZE * 0.03
        ], fill=(85, 47, 115), outline=(55, 35, 85), width=2)
    
    # Central energy orb (large, floating above temple)
    orb_x = CENTER
    orb_y = platform_y - SIZE * 0.08 - temple_height * 0.7 - SIZE * 0.25
    orb_radius = SIZE * 0.06
    
    # Orb glow layers
    for r in range(int(orb_radius * 3), int(orb_radius), -5):
        alpha = 100 - r
        draw.ellipse([
            orb_x - r, orb_y - r,
            orb_x + r, orb_y + r
        ], outline=(180, 80, 220, alpha), width=2)
    
    # Orb core
    draw.ellipse([
        orb_x - orb_radius, orb_y - orb_radius,
        orb_x + orb_radius, orb_y + orb_radius
    ], fill=(200, 100, 255))
    
    # Orb inner glow
    draw.ellipse([
        orb_x - orb_radius * 0.7, orb_y - orb_radius * 0.7,
        orb_x + orb_radius * 0.7, orb_y + orb_radius * 0.7
    ], fill=(220, 150, 255))
    
    # Orb bright center
    draw.ellipse([
        orb_x - orb_radius * 0.3, orb_y - orb_radius * 0.3,
        orb_x + orb_radius * 0.3, orb_y + orb_radius * 0.3
    ], fill=(255, 220, 255))
    
    # Energy beams (radiating from orb)
    beam_count = 8
    for i in range(beam_count):
        angle = i * 2 * math.pi / beam_count
        beam_length = SIZE * 0.25
        
        start_x = orb_x + math.cos(angle) * orb_radius
        start_y = orb_y + math.sin(angle) * orb_radius
        end_x = orb_x + math.cos(angle) * (orb_radius + beam_length)
        end_y = orb_y + math.sin(angle) * (orb_radius + beam_length)
        
        # Beam with gradient effect
        draw.line([
            (start_x, start_y),
            (end_x, end_y)
        ], fill=(180, 80, 220), width=4)
        
        # Beam glow
        draw.line([
            (start_x, start_y),
            (end_x * 0.9 + orb_x * 0.1, end_y * 0.9 + orb_y * 0.1)
        ], fill=(200, 120, 240, 100), width=6)
    
    # Smaller floating orbs
    for ox, oy in [
        (CENTER - SIZE * 0.2, SIZE * 0.4),
        (CENTER + SIZE * 0.2, SIZE * 0.42),
        (CENTER - SIZE * 0.15, SIZE * 0.35),
        (CENTER + SIZE * 0.15, SIZE * 0.37)
    ]:
        small_orb_r = SIZE * 0.025
        
        # Glow
        draw.ellipse([
            ox - small_orb_r * 2, oy - small_orb_r * 2,
            ox + small_orb_r * 2, oy + small_orb_r * 2
        ], outline=(160, 70, 200, 100), width=2)
        
        # Core
        draw.ellipse([
            ox - small_orb_r, oy - small_orb_r,
            ox + small_orb_r, oy + small_orb_r
        ], fill=(180, 90, 230))
        
        # Bright center
        draw.ellipse([
            ox - small_orb_r * 0.4, oy - small_orb_r * 0.4,
            ox + small_orb_r * 0.4, oy + small_orb_r * 0.4
        ], fill=(230, 180, 255))
    
    # Mystical particles
    for _ in range(20):
        px = random.uniform(SIZE * 0.3, SIZE * 0.7)
        py = random.uniform(SIZE * 0.3, SIZE * 0.65)
        pr = random.uniform(2, 5)
        draw.ellipse([
            px - pr, py - pr, px + pr, py + pr
        ], fill=(200, 120, 255, 180))
    
    # Add golden frame
    draw_golden_frame(draw)
    
    img.save(f"{OUTPUT_DIR}void_temple.png", "PNG")
    print("✓ void_temple.png created")

def main():
    print("Starting Crimson Empire Icon Generation...")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Canvas size: {SIZE}x{SIZE}")
    print()
    
    # Generate all 8 icons
    draw_border_outpost()
    draw_bandit_camp()
    draw_abandoned_castle()
    draw_orc_tribe()
    draw_dark_fortress()
    draw_dragon_lair()
    draw_demon_throne()
    draw_void_temple()
    
    print()
    print("All icons generated successfully!")
    print("Design philosophy: Crimson Empire - Luminous Dark Fantasy")

if __name__ == "__main__":
    main()

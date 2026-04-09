#!/usr/bin/env python3
"""
Generate 8 territory icons for Conqueror game - Crimson Empire style
NO golden rings/borders - clean square icons with vibrant colors
1024x1024 PNG, main subject fills 70-80% of canvas
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

OUTPUT_DIR = "/root/.openclaw/workspace/game_public/icons_new"
SIZE = 1024
CENTER = SIZE // 2

def create_gradient_background(colors, direction='vertical'):
    """Create a gradient background"""
    base = Image.new('RGB', (SIZE, SIZE), colors[0])
    draw = ImageDraw.Draw(base)
    
    if direction == 'vertical':
        for y in range(SIZE):
            ratio = y / SIZE
            r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
            draw.line([(0, y), (SIZE, y)], fill=(r, g, b))
    elif direction == 'radial':
        for y in range(SIZE):
            for x in range(SIZE):
                dist = math.sqrt((x - CENTER)**2 + (y - CENTER)**2) / (SIZE * 0.7)
                dist = min(dist, 1)
                r = int(colors[0][0] * (1-dist) + colors[1][0] * dist)
                g = int(colors[0][1] * (1-dist) + colors[1][1] * dist)
                b = int(colors[0][2] * (1-dist) + colors[1][2] * dist)
                draw.point((x, y), fill=(r, g, b))
    
    return base

def draw_border_outpost():
    """边境哨站 - Golden watchtower, red flags, lookout"""
    img = create_gradient_background([(40, 60, 120), (80, 120, 180)], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Tower base (stone gray with golden highlights)
    tower_points = [
        (CENTER - 120, SIZE - 150),
        (CENTER + 120, SIZE - 150),
        (CENTER + 100, SIZE - 450),
        (CENTER - 100, SIZE - 450),
    ]
    draw.polygon(tower_points, fill=(180, 170, 160))
    draw.polygon(tower_points, outline=(200, 190, 180), width=3)
    
    # Tower top platform
    draw.rectangle([CENTER - 140, SIZE - 470, CENTER + 140, SIZE - 440], fill=(160, 150, 140))
    
    # Golden roof/spire
    spire_points = [
        (CENTER - 80, SIZE - 470),
        (CENTER + 80, SIZE - 470),
        (CENTER, SIZE - 650),
    ]
    draw.polygon(spire_points, fill=(218, 165, 32), outline=(255, 215, 0), width=2)
    
    # Red flag on left
    flag_pole_left = [(CENTER - 140, SIZE - 460), (CENTER - 140, SIZE - 580)]
    draw.line(flag_pole_left, fill=(139, 69, 19), width=8)
    flag_left = [
        (CENTER - 140, SIZE - 580),
        (CENTER - 280, SIZE - 540),
        (CENTER - 140, SIZE - 500),
    ]
    draw.polygon(flag_left, fill=(220, 20, 60), outline=(180, 10, 40), width=2)
    
    # Red flag on right
    flag_pole_right = [(CENTER + 140, SIZE - 460), (CENTER + 140, SIZE - 580)]
    draw.line(flag_pole_right, fill=(139, 69, 19), width=8)
    flag_right = [
        (CENTER + 140, SIZE - 580),
        (CENTER + 280, SIZE - 540),
        (CENTER + 140, SIZE - 500),
    ]
    draw.polygon(flag_right, fill=(220, 20, 60), outline=(180, 10, 40), width=2)
    
    # Watch windows (glowing)
    draw.rectangle([CENTER - 60, SIZE - 400, CENTER - 20, SIZE - 340], fill=(255, 200, 100))
    draw.rectangle([CENTER + 20, SIZE - 400, CENTER + 60, SIZE - 340], fill=(255, 200, 100))
    
    # Battlements
    for i in range(-3, 4):
        bx = CENTER + i * 40
        draw.rectangle([bx - 15, SIZE - 490, bx + 15, SIZE - 470], fill=(170, 160, 150))
    
    return img

def draw_bandit_camp():
    """强盗营地 - Brown tents, campfire, camp elements"""
    img = create_gradient_background([(80, 50, 30), (120, 80, 50)], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Ground
    draw.rectangle([0, SIZE - 100, SIZE, SIZE], fill=(60, 40, 20))
    
    # Main tent (large brown)
    tent_base = [(CENTER - 200, SIZE - 150), (CENTER + 200, SIZE - 150), (CENTER, SIZE - 450)]
    draw.polygon(tent_base, fill=(139, 90, 43), outline=(100, 60, 30), width=3)
    
    # Tent entrance (dark)
    entrance = [
        (CENTER - 50, SIZE - 150),
        (CENTER + 50, SIZE - 150),
        (CENTER + 40, SIZE - 280),
        (CENTER - 40, SIZE - 280),
    ]
    draw.polygon(entrance, fill=(50, 30, 15))
    
    # Tent stripes
    for i in range(-3, 4):
        if i != 0:
            stripe_y = SIZE - 150 + i * 50
            if stripe_y > SIZE - 400:
                stripe_width = 100 - abs(i) * 15
                draw.line([
                    (CENTER - stripe_width, stripe_y),
                    (CENTER + stripe_width, stripe_y)
                ], fill=(100, 60, 30), width=4)
    
    # Small tent left
    small_tent_l = [(CENTER - 320, SIZE - 120), (CENTER - 220, SIZE - 120), (CENTER - 270, SIZE - 240)]
    draw.polygon(small_tent_l, fill=(120, 80, 40), outline=(80, 50, 25), width=2)
    
    # Small tent right
    small_tent_r = [(CENTER + 220, SIZE - 120), (CENTER + 320, SIZE - 120), (CENTER + 270, SIZE - 240)]
    draw.polygon(small_tent_r, fill=(120, 80, 40), outline=(80, 50, 25), width=2)
    
    # Campfire (center front)
    # Fire base (stones)
    draw.ellipse([CENTER - 60, SIZE - 100, CENTER + 60, SIZE - 40], fill=(50, 50, 50))
    
    # Flames
    flame_colors = [(255, 100, 0), (255, 150, 0), (255, 200, 50)]
    for i, color in enumerate(flame_colors):
        flame_h = 80 - i * 20
        flame = [
            (CENTER - 30 + i*5, SIZE - 80),
            (CENTER + 30 - i*5, SIZE - 80),
            (CENTER, SIZE - 80 - flame_h),
        ]
        draw.polygon(flame, fill=color)
    
    # Wooden stakes around camp
    for i in range(-2, 3):
        stake_x = CENTER + i * 80
        if abs(i) > 0:
            draw.rectangle([stake_x - 8, SIZE - 140, stake_x + 8, SIZE - 80], fill=(101, 67, 33))
    
    return img

def draw_abandoned_castle():
    """废弃城堡 - Broken twin towers, moonlight, ruins"""
    img = create_gradient_background([(30, 30, 60), (80, 80, 120)], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Moon (large, glowing)
    draw.ellipse([CENTER - 100, 100, CENTER + 100, 300], fill=(240, 240, 250))
    draw.ellipse([CENTER - 90, 110, CENTER + 90, 290], fill=(255, 255, 255))
    
    # Left tower (broken)
    left_tower = [
        (CENTER - 280, SIZE - 100),
        (CENTER - 180, SIZE - 100),
        (CENTER - 160, SIZE - 500),
        (CENTER - 300, SIZE - 500),
    ]
    draw.polygon(left_tower, fill=(80, 80, 90), outline=(60, 60, 70), width=2)
    
    # Broken top left
    draw.line([
        (CENTER - 300, SIZE - 500),
        (CENTER - 250, SIZE - 550),
        (CENTER - 200, SIZE - 520),
        (CENTER - 160, SIZE - 500),
    ], fill=(70, 70, 80), width=3)
    
    # Right tower (broken)
    right_tower = [
        (CENTER + 180, SIZE - 100),
        (CENTER + 280, SIZE - 100),
        (CENTER + 300, SIZE - 500),
        (CENTER + 160, SIZE - 500),
    ]
    draw.polygon(right_tower, fill=(80, 80, 90), outline=(60, 60, 70), width=2)
    
    # Broken top right
    draw.line([
        (CENTER + 160, SIZE - 500),
        (CENTER + 200, SIZE - 520),
        (CENTER + 250, SIZE - 550),
        (CENTER + 300, SIZE - 500),
    ], fill=(70, 70, 80), width=3)
    
    # Connecting wall (ruined)
    draw.rectangle([CENTER - 160, SIZE - 350, CENTER + 160, SIZE - 300], fill=(70, 70, 80))
    
    # Cracks in wall
    draw.line([(CENTER - 100, SIZE - 350), (CENTER - 80, SIZE - 300)], fill=(40, 40, 50), width=2)
    draw.line([(CENTER + 50, SIZE - 350), (CENTER + 80, SIZE - 300)], fill=(40, 40, 50), width=2)
    
    # Broken archway
    arch = [
        (CENTER - 80, SIZE - 100),
        (CENTER - 80, SIZE - 300),
        (CENTER - 60, SIZE - 320),
        (CENTER + 60, SIZE - 320),
        (CENTER + 80, SIZE - 300),
        (CENTER + 80, SIZE - 100),
    ]
    draw.polygon(arch, fill=(50, 50, 60))
    
    # Windows (dark, broken)
    for i in range(-2, 3):
        if abs(i) > 0:
            win_x = CENTER + i * 100
            draw.rectangle([win_x - 20, SIZE - 450, win_x + 20, SIZE - 380], fill=(20, 20, 30))
    
    # Debris at base
    for i in range(-4, 5):
        if i != 0:
            debris_x = CENTER + i * 60
            debris_h = 20 + abs(i) * 5
            draw.polygon([
                (debris_x - 20, SIZE - 50),
                (debris_x + 20, SIZE - 50),
                (debris_x + 15, SIZE - 50 - debris_h),
                (debris_x - 15, SIZE - 50 - debris_h),
            ], fill=(60, 60, 70))
    
    return img

def draw_orc_tribe():
    """兽人部落 - Totem poles, skulls, green energy"""
    img = create_gradient_background([(20, 50, 20), (60, 100, 40)], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Ground
    draw.rectangle([0, SIZE - 80, SIZE, SIZE], fill=(40, 30, 20))
    
    # Central totem pole
    totem_base = [(CENTER - 50, SIZE - 80), (CENTER + 50, SIZE - 80), (CENTER + 40, SIZE - 550), (CENTER - 40, SIZE - 550)]
    draw.polygon(totem_base, fill=(80, 60, 40), outline=(60, 40, 25), width=2)
    
    # Skull on totem (top)
    skull_y = SIZE - 480
    draw.ellipse([CENTER - 45, skull_y - 60, CENTER + 45, skull_y + 20], fill=(200, 200, 190))
    # Eye sockets
    draw.ellipse([CENTER - 30, skull_y - 40, CENTER - 10, skull_y - 15], fill=(30, 30, 30))
    draw.ellipse([CENTER + 10, skull_y - 40, CENTER + 30, skull_y - 15], fill=(30, 30, 30))
    # Nose
    draw.polygon([(CENTER, skull_y - 10), (CENTER - 8, skull_y + 5), (CENTER + 8, skull_y + 5)], fill=(30, 30, 30))
    # Teeth
    draw.line([(CENTER - 25, skull_y + 15), (CENTER + 25, skull_y + 15)], fill=(30, 30, 30), width=3)
    for i in range(-2, 3):
        draw.line([(CENTER + i*10, skull_y + 15), (CENTER + i*10, skull_y + 25)], fill=(30, 30, 30), width=2)
    
    # Green energy aura around skull
    for i in range(3):
        aura_size = 75 + i * 15
        alpha = 80 - i * 25
        draw.ellipse([CENTER - aura_size, skull_y - 70, CENTER + aura_size, skull_y + 30], 
                    fill=(0, 255, 100, alpha))
    
    # Tribal symbols on totem
    for i in range(3):
        sym_y = SIZE - 350 + i * 80
        # V shape
        draw.line([(CENTER - 30, sym_y - 20), (CENTER, sym_y + 10), (CENTER + 30, sym_y - 20)], 
                   fill=(150, 100, 50), width=5)
    
    # Side totems (smaller)
    for side in [-1, 1]:
        side_x = CENTER + side * 200
        small_totem = [(side_x - 30, SIZE - 80), (side_x + 30, SIZE - 80), 
                       (side_x + 25, SIZE - 350), (side_x - 25, SIZE - 350)]
        draw.polygon(small_totem, fill=(70, 50, 35), outline=(50, 35, 20), width=2)
        
        # Small skull
        small_skull_y = SIZE - 300
        draw.ellipse([side_x - 25, small_skull_y - 35, side_x + 25, small_skull_y + 10], fill=(190, 190, 180))
        draw.ellipse([side_x - 15, small_skull_y - 25, side_x - 5, small_skull_y - 12], fill=(30, 30, 30))
        draw.ellipse([side_x + 5, small_skull_y - 25, side_x + 15, small_skull_y - 12], fill=(30, 30, 30))
    
    # Green energy particles
    import random
    random.seed(42)
    for _ in range(30):
        px = CENTER + random.randint(-300, 300)
        py = random.randint(SIZE - 500, SIZE - 100)
        ps = random.randint(3, 8)
        draw.ellipse([px - ps, py - ps, px + ps, py + ps], fill=(0, 255, 100, 150))
    
    return img

def draw_dark_fortress():
    """黑暗要塞 - Solid walls, golden window lights"""
    img = create_gradient_background([(40, 30, 60), (80, 60, 100)], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Main fortress wall
    wall_base = [
        (CENTER - 350, SIZE - 100),
        (CENTER + 350, SIZE - 100),
        (CENTER + 320, SIZE - 550),
        (CENTER - 320, SIZE - 550),
    ]
    draw.polygon(wall_base, fill=(60, 50, 70), outline=(80, 70, 90), width=3)
    
    # Battlements on top
    for i in range(-7, 8):
        bx = CENTER + i * 45
        draw.rectangle([bx - 18, SIZE - 570, bx + 18, SIZE - 550], fill=(50, 40, 60))
    
    # Central gate (dark arch)
    gate = [
        (CENTER - 100, SIZE - 100),
        (CENTER - 100, SIZE - 350),
        (CENTER - 80, SIZE - 380),
        (CENTER + 80, SIZE - 380),
        (CENTER + 100, SIZE - 350),
        (CENTER + 100, SIZE - 100),
    ]
    draw.polygon(gate, fill=(30, 25, 40))
    
    # Gate details (wooden doors)
    draw.rectangle([CENTER - 90, SIZE - 340, CENTER - 10, SIZE - 110], fill=(50, 35, 25))
    draw.rectangle([CENTER + 10, SIZE - 340, CENTER + 90, SIZE - 110], fill=(50, 35, 25))
    
    # Golden window lights (multiple rows)
    window_rows = [
        (SIZE - 480, [-200, -100, 100, 200]),
        (SIZE - 350, [-250, -150, 150, 250]),
        (SIZE - 220, [-220, -120, 120, 220]),
    ]
    
    for row_y, offsets in window_rows:
        for offset in offsets:
            wx = CENTER + offset
            # Window frame
            draw.rectangle([wx - 20, row_y - 35, wx + 20, row_y + 15], fill=(40, 35, 50))
            # Golden glow inside
            draw.rectangle([wx - 15, row_y - 30, wx + 15, row_y + 10], fill=(255, 200, 80))
            # Bright center
            draw.rectangle([wx - 8, row_y - 22, wx + 8, row_y + 2], fill=(255, 230, 150))
    
    # Side towers
    for side in [-1, 1]:
        tower_x = CENTER + side * 280
        tower = [
            (tower_x - 70, SIZE - 100),
            (tower_x + 70, SIZE - 100),
            (tower_x + 60, SIZE - 450),
            (tower_x - 60, SIZE - 450),
        ]
        draw.polygon(tower, fill=(55, 45, 65), outline=(75, 65, 85), width=2)
        
        # Tower windows (glowing)
        for wy in [SIZE - 400, SIZE - 300, SIZE - 200]:
            draw.rectangle([tower_x - 20, wy - 25, tower_x + 20, wy + 15], fill=(255, 190, 60))
            draw.rectangle([tower_x - 12, wy - 18, tower_x + 12, wy + 8], fill=(255, 220, 100))
        
        # Tower roof (pointed)
        roof = [
            (tower_x - 75, SIZE - 450),
            (tower_x + 75, SIZE - 450),
            (tower_x, SIZE - 580),
        ]
        draw.polygon(roof, fill=(50, 40, 60), outline=(70, 60, 80), width=2)
    
    return img

def draw_dragon_lair():
    """龙之巢穴 - Red dragon shadow, golden horns, flames"""
    img = create_gradient_background([(80, 30, 20), (150, 60, 30)], 'radial')
    draw = ImageDraw.Draw(img)
    
    # Cave background (darker)
    draw.ellipse([CENTER - 450, CENTER - 450, CENTER + 450, CENTER + 450], fill=(40, 15, 10))
    
    # Dragon head silhouette (facing left)
    dragon_points = [
        (CENTER + 100, SIZE - 200),  # neck base
        (CENTER + 50, SIZE - 300),   # neck
        (CENTER - 50, SIZE - 350),   # jaw
        (CENTER - 150, SIZE - 320),  # snout
        (CENTER - 180, SIZE - 380),  # nose
        (CENTER - 150, SIZE - 420),  # top snout
        (CENTER - 50, SIZE - 450),   # forehead
        (CENTER + 50, SIZE - 420),   # back head
        (CENTER + 100, SIZE - 350),  # back neck
        (CENTER + 80, SIZE - 250),   # neck front
    ]
    draw.polygon(dragon_points, fill=(60, 20, 15))
    
    # Golden horns
    horn1 = [
        (CENTER - 30, SIZE - 450),
        (CENTER - 60, SIZE - 580),
        (CENTER - 20, SIZE - 560),
        (CENTER + 10, SIZE - 440),
    ]
    draw.polygon(horn1, fill=(218, 165, 32), outline=(255, 215, 0), width=2)
    
    horn2 = [
        (CENTER + 20, SIZE - 430),
        (CENTER - 10, SIZE - 560),
        (CENTER + 30, SIZE - 580),
        (CENTER + 60, SIZE - 450),
    ]
    draw.polygon(horn2, fill=(218, 165, 32), outline=(255, 215, 0), width=2)
    
    # Glowing eye
    eye_x = CENTER - 80
    eye_y = SIZE - 400
    draw.ellipse([eye_x - 15, eye_y - 15, eye_x + 25, eye_y + 15], fill=(255, 200, 50))
    draw.ellipse([eye_x - 5, eye_y - 8, eye_x + 15, eye_y + 8], fill=(255, 100, 0))
    draw.rectangle([eye_x + 5, eye_y - 10, eye_x + 12, eye_y + 10], fill=(0, 0, 0))  # pupil
    
    # Flames from mouth
    flame_base_x = CENTER - 140
    flame_base_y = SIZE - 330
    
    for i in range(5):
        flame_len = 120 - i * 15
        flame_angle = -0.3 + i * 0.15
        fx_end = flame_base_x - flame_len * math.cos(flame_angle)
        fy_end = flame_base_y - flame_len * math.sin(flame_angle)
        
        flame_width = 40 - i * 6
        flame = [
            (flame_base_x, flame_base_y),
            (fx_end - flame_width/2, fy_end),
            (fx_end, fy_end - flame_width),
            (fx_end + flame_width/2, fy_end),
        ]
        
        if i == 0:
            color = (255, 200, 50)
        elif i == 1:
            color = (255, 150, 30)
        elif i == 2:
            color = (255, 100, 20)
        else:
            color = (255, 50, 10)
        
        draw.polygon(flame, fill=color)
    
    # Treasure pile (gold coins)
    for i in range(20):
        import random
        random.seed(i + 100)
        cx = CENTER + 150 + random.randint(-100, 200)
        cy = SIZE - 150 + random.randint(-50, 50)
        cr = random.randint(15, 30)
        draw.ellipse([cx - cr, cy - cr/2, cx + cr, cy + cr/2], fill=(218, 165, 32))
        draw.ellipse([cx - cr + 3, cy - cr/2 + 2, cx + cr - 5, cy + cr/2 - 2], fill=(255, 215, 0))
    
    return img

def draw_demon_throne():
    """恶魔王座 - Purple throne, red demon symbols"""
    img = create_gradient_background([(50, 20, 60), (100, 40, 120)], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Steps/platform
    for i in range(3):
        step_y = SIZE - 100 + i * 40
        step_h = 35
        draw.rectangle([CENTER - 200 + i*30, step_y, CENTER + 200 - i*30, step_y + step_h], 
                      fill=(60, 30, 70))
        draw.line([CENTER - 200 + i*30, step_y, CENTER + 200 - i*30, step_y], 
                 fill=(80, 50, 90), width=2)
    
    # Throne base
    throne_base = [
        (CENTER - 120, SIZE - 200),
        (CENTER + 120, SIZE - 200),
        (CENTER + 100, SIZE - 350),
        (CENTER - 100, SIZE - 350),
    ]
    draw.polygon(throne_base, fill=(70, 30, 90), outline=(90, 50, 110), width=3)
    
    # Throne back (tall)
    throne_back = [
        (CENTER - 100, SIZE - 350),
        (CENTER + 100, SIZE - 350),
        (CENTER + 80, SIZE - 600),
        (CENTER - 80, SIZE - 600),
    ]
    draw.polygon(throne_back, fill=(60, 25, 80), outline=(85, 45, 105), width=3)
    
    # Throne arms
    for side in [-1, 1]:
        arm_x = CENTER + side * 110
        draw.polygon([
            (arm_x - 25, SIZE - 200),
            (arm_x + 25, SIZE - 200),
            (arm_x + 20, SIZE - 350),
            (arm_x - 20, SIZE - 350),
        ], fill=(65, 28, 85))
    
    # Demon symbol on throne back (large pentagram-like)
    symbol_center_y = SIZE - 475
    # Outer circle (faint)
    draw.ellipse([CENTER - 70, symbol_center_y - 70, CENTER + 70, symbol_center_y + 70], 
                fill=None, outline=(150, 50, 80), width=3)
    
    # Pentagram
    import math
    pentagon_points = []
    for i in range(5):
        angle = -math.pi/2 + i * 2 * math.pi / 5
        px = CENTER + 60 * math.cos(angle)
        py = symbol_center_y + 60 * math.sin(angle)
        pentagon_points.append((px, py))
    
    # Draw star
    for i in range(5):
        draw.line([pentagon_points[i], pentagon_points[(i+2) % 5]], 
                 fill=(220, 30, 60), width=5)
    
    # Center circle (glowing red)
    draw.ellipse([CENTER - 20, symbol_center_y - 20, CENTER + 20, symbol_center_y + 20], 
                fill=(255, 50, 80))
    draw.ellipse([CENTER - 12, symbol_center_y - 12, CENTER + 12, symbol_center_y + 12], 
                fill=(255, 100, 120))
    
    # Purple cushion on seat
    draw.ellipse([CENTER - 80, SIZE - 230, CENTER + 80, SIZE - 180], fill=(90, 40, 110))
    draw.ellipse([CENTER - 70, SIZE - 225, CENTER + 70, SIZE - 185], fill=(110, 50, 130))
    
    # Floating demon runes around throne
    rune_positions = [
        (CENTER - 200, SIZE - 400),
        (CENTER + 200, SIZE - 400),
        (CENTER - 180, SIZE - 500),
        (CENTER + 180, SIZE - 500),
        (CENTER, SIZE - 550),
    ]
    
    for rx, ry in rune_positions:
        # Glowing rune symbol (simplified)
        draw.ellipse([rx - 25, ry - 25, rx + 25, ry + 25], fill=(80, 20, 100, 100))
        draw.line([(rx - 15, ry - 15), (rx + 15, ry + 15)], fill=(255, 80, 120), width=3)
        draw.line([(rx + 15, ry - 15), (rx - 15, ry + 15)], fill=(255, 80, 120), width=3)
    
    # Ethereal purple flames at base
    for i in range(7):
        flame_x = CENTER - 180 + i * 60
        flame_h = 40 + abs(i - 3) * 10
        draw.polygon([
            (flame_x - 20, SIZE - 200),
            (flame_x + 20, SIZE - 200),
            (flame_x, SIZE - 200 - flame_h),
        ], fill=(150, 50, 180, 180))
    
    return img

def draw_void_temple():
    """虚空神殿 - Purple temple, energy orbs and beams"""
    img = create_gradient_background([(30, 20, 60), (80, 40, 120)], 'vertical')
    draw = ImageDraw.Draw(img)
    
    # Temple platform
    draw.rectangle([CENTER - 300, SIZE - 120, CENTER + 300, SIZE - 80], fill=(70, 40, 100))
    draw.rectangle([CENTER - 280, SIZE - 160, CENTER + 280, SIZE - 120], fill=(60, 35, 90))
    
    # Main temple structure
    temple_base = [
        (CENTER - 200, SIZE - 160),
        (CENTER + 200, SIZE - 160),
        (CENTER + 180, SIZE - 450),
        (CENTER - 180, SIZE - 450),
    ]
    draw.polygon(temple_base, fill=(80, 50, 120), outline=(100, 70, 140), width=3)
    
    # Temple entrance (glowing void)
    entrance = [
        (CENTER - 60, SIZE - 160),
        (CENTER - 60, SIZE - 380),
        (CENTER - 50, SIZE - 400),
        (CENTER + 50, SIZE - 400),
        (CENTER + 60, SIZE - 380),
        (CENTER + 60, SIZE - 160),
    ]
    draw.polygon(entrance, fill=(40, 10, 60))
    # Inner glow
    draw.ellipse([CENTER - 50, SIZE - 390, CENTER + 50, SIZE - 170], fill=(100, 50, 150, 100))
    
    # Columns (left and right)
    for side in [-1, 1]:
        col_x = CENTER + side * 140
        # Column shaft
        draw.rectangle([col_x - 25, SIZE - 450, col_x + 25, SIZE - 160], fill=(70, 45, 110))
        # Column capital
        draw.rectangle([col_x - 30, SIZE - 460, col_x + 30, SIZE - 450], fill=(90, 60, 130))
        # Column base
        draw.rectangle([col_x - 30, SIZE - 160, col_x + 30, SIZE - 140], fill=(90, 60, 130))
        # Glowing runes on column
        for ry in [SIZE - 380, SIZE - 300, SIZE - 220]:
            draw.rectangle([col_x - 10, ry - 15, col_x + 10, ry + 15], fill=(180, 100, 255, 150))
    
    # Temple roof (triangular)
    roof = [
        (CENTER - 220, SIZE - 450),
        (CENTER + 220, SIZE - 450),
        (CENTER, SIZE - 600),
    ]
    draw.polygon(roof, fill=(70, 45, 110), outline=(95, 65, 135), width=3)
    
    # Roof peak (energy orb)
    orb_y = SIZE - 600
    # Outer glow
    draw.ellipse([CENTER - 50, orb_y - 50, CENTER + 50, orb_y + 50], fill=(150, 80, 255, 100))
    # Main orb
    draw.ellipse([CENTER - 35, orb_y - 35, CENTER + 35, orb_y + 35], fill=(180, 100, 255))
    # Inner bright core
    draw.ellipse([CENTER - 20, orb_y - 20, CENTER + 20, orb_y + 20], fill=(220, 180, 255))
    # Core highlight
    draw.ellipse([CENTER - 10, orb_y - 10, CENTER + 10, orb_y + 10], fill=(255, 230, 255))
    
    # Energy beams shooting up
    for i in range(5):
        beam_x = CENTER - 100 + i * 50
        beam_width = 15 - abs(i - 2) * 2
        draw.polygon([
            (beam_x - beam_width, orb_y - 50),
            (beam_x + beam_width, orb_y - 50),
            (beam_x + beam_width/2, 50),
            (beam_x - beam_width/2, 50),
        ], fill=(180, 120, 255, 150))
    
    # Floating energy orbs around temple
    orb_positions = [
        (CENTER - 280, SIZE - 350),
        (CENTER + 280, SIZE - 350),
        (CENTER - 320, SIZE - 250),
        (CENTER + 320, SIZE - 250),
        (CENTER, SIZE - 280),
    ]
    
    for ox, oy in orb_positions:
        orb_size = 25
        # Glow
        draw.ellipse([ox - orb_size - 5, oy - orb_size - 5, 
                     ox + orb_size + 5, oy + orb_size + 5], fill=(150, 80, 255, 80))
        # Orb
        draw.ellipse([ox - orb_size, oy - orb_size, ox + orb_size, oy + orb_size], fill=(180, 100, 255))
        # Highlight
        draw.ellipse([ox - orb_size/2, oy - orb_size/2, 
                     ox + orb_size/2, oy + orb_size/2], fill=(220, 180, 255))
    
    # Energy arcs connecting orbs
    draw.arc([CENTER - 350, SIZE - 450, CENTER + 350, SIZE - 150], 
            180, 360, fill=(150, 100, 255), width=3)
    
    # Mystical particles
    import random
    random.seed(77)
    for _ in range(40):
        px = CENTER + random.randint(-350, 350)
        py = random.randint(100, SIZE - 200)
        ps = random.randint(2, 6)
        draw.ellipse([px - ps, py - ps, px + ps, py + ps], fill=(200, 150, 255, 180))
    
    return img

def main():
    icons = {
        'border_outpost': draw_border_outpost,
        'bandit_camp': draw_bandit_camp,
        'abandoned_castle': draw_abandoned_castle,
        'orc_tribe': draw_orc_tribe,
        'dark_fortress': draw_dark_fortress,
        'dragon_lair': draw_dragon_lair,
        'demon_throne': draw_demon_throne,
        'void_temple': draw_void_temple,
    }
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for name, draw_func in icons.items():
        print(f"Generating {name}...")
        img = draw_func()
        output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
        img.save(output_path, 'PNG')
        print(f"  Saved to {output_path}")
    
    print("\nAll icons generated successfully!")

if __name__ == '__main__':
    main()

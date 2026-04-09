#!/usr/bin/env python3
"""
《征服者》领地图标生成器
生成 8 个 1024x1024 的明亮风格领地图标
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

OUTPUT_DIR = "/root/.openclaw/workspace/game_public/icons_new"

def create_gradient_background(width, height, color1, color2):
    """创建垂直渐变背景"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def draw_golden_ring(draw, center, outer_radius, inner_radius):
    """绘制金色圆环"""
    cx, cy = center
    
    # 外圆
    for r in range(inner_radius, outer_radius + 1):
        angle_offset = 0
        for angle in range(0, 360, 2):
            rad = math.radians(angle + angle_offset)
            x1 = cx + int(r * math.cos(rad))
            y1 = cy + int(r * math.sin(rad))
            x2 = cx + int((r + 1) * math.cos(rad))
            y2 = cy + int((r + 1) * math.sin(rad))
            
            # 金色渐变效果
            brightness = int(200 + 55 * math.sin(math.radians(angle * 3)))
            draw.line([(x1, y1), (x2, y2)], fill=(255, min(255, brightness + 50), max(100, brightness - 50)))

def draw_silver_ring(draw, center, outer_radius, inner_radius):
    """绘制银色圆环"""
    cx, cy = center
    
    for r in range(inner_radius, outer_radius + 1):
        for angle in range(0, 360, 2):
            rad = math.radians(angle)
            x1 = cx + int(r * math.cos(rad))
            y1 = cy + int(r * math.sin(rad))
            x2 = cx + int((r + 1) * math.cos(rad))
            y2 = cy + int((r + 1) * math.sin(rad))
            
            brightness = int(200 + 55 * math.sin(math.radians(angle * 3)))
            draw.line([(x1, y1), (x2, y2)], fill=(brightness, brightness, min(255, brightness + 30)))

def draw_border_outpost():
    """1. 边境哨站 - 哨塔、瞭望台"""
    img = create_gradient_background(1024, 1024, (45, 27, 105), (26, 26, 62))
    draw = ImageDraw.Draw(img)
    
    # 金色外环
    draw_golden_ring(draw, (512, 512), 500, 420)
    
    # 哨塔主体
    for y in range(350, 700):
        brightness = int(135 + (y - 350) * 0.1)
        draw.rectangle([(460, y), (564, y + 1)], fill=(brightness, min(200, 130 + brightness // 2), min(255, 180 + brightness // 3)))
    
    # 塔顶（金色）
    points = [(440, 350), (512, 280), (584, 350)]
    draw.polygon(points, fill=(255, 215, 0))
    
    # 瞭望台
    draw.rectangle([(430, 400), (594, 440)], fill=(192, 192, 192))
    
    # 旗杆
    draw.line([(512, 280), (512, 200)], fill=(255, 69, 0), width=8)
    
    # 旗帜
    flag_points = [(512, 200), (600, 230), (512, 260)]
    draw.polygon(flag_points, fill=(255, 69, 0))
    
    # 顶部光晕
    for r in range(30, 0, -2):
        alpha = int(100 * (r / 30))
        draw.ellipse([(512-r, 280-r), (512+r, 280+r)], fill=(255, 255, 0, alpha))
    
    return img

def draw_bandit_camp():
    """2. 强盗营地 - 帐篷、篝火"""
    img = create_gradient_background(1024, 1024, (61, 31, 31), (42, 26, 26))
    draw = ImageDraw.Draw(img)
    
    # 银色外环
    draw_silver_ring(draw, (512, 512), 500, 420)
    
    # 帐篷主体
    tent_points = [(512, 300), (350, 650), (674, 650)]
    draw.polygon(tent_points, fill=(139, 69, 19))
    
    # 帐篷条纹
    for i in range(-2, 3):
        x_offset = i * 60
        draw.line([(450 + x_offset, 400), (480 + x_offset, 650)], fill=(205, 133, 63), width=15)
    
    # 篝火 base
    for r in range(80, 0, -2):
        color_val = int(255 * (r / 80))
        draw.ellipse([(512-r, 700-r), (512+r, 700+r)], fill=(255, color_val, 0))
    
    # 火焰
    flame_points = [(512, 650), (540, 600), (512, 560), (484, 600)]
    draw.polygon(flame_points, fill=(255, 215, 0))
    
    return img

def draw_abandoned_castle():
    """3. 废弃城堡 - 破败城堡"""
    img = create_gradient_background(1024, 1024, (58, 58, 90), (42, 42, 74))
    draw = ImageDraw.Draw(img)
    
    # 金色外环
    draw_golden_ring(draw, (512, 512), 500, 420)
    
    # 城堡主体
    for y in range(400, 750):
        brightness = int(112 - (y - 400) * 0.1)
        draw.rectangle([(380, y), (644, y + 1)], fill=(brightness, min(140, brightness + 28), min(160, brightness + 48)))
    
    # 左塔楼
    draw.rectangle([(350, 350), (450, 550)], fill=(96, 112, 128))
    draw.ellipse([(340, 290), (460, 410)], fill=(96, 112, 128))
    
    # 右塔楼
    draw.rectangle([(574, 350), (674, 550)], fill=(96, 112, 128))
    draw.ellipse([(564, 290), (684, 410)], fill=(96, 112, 128))
    
    # 破损窗口
    draw.rectangle([(450, 450), (480, 530)], fill=(42, 42, 74))
    draw.rectangle([(544, 450), (574, 530)], fill=(42, 42, 74))
    
    # 中央大门
    draw.rectangle([(452, 690), (572, 750)], fill=(58, 58, 90))
    draw.arc([(452, 690), (572, 810)], 0, 180, fill=(58, 58, 90), width=60)
    
    # 月光
    draw.ellipse([(650, 200), (750, 300)], fill=(224, 224, 224, 76))
    
    return img

def draw_orc_tribe():
    """4. 兽人部落 - 兽人图腾"""
    img = create_gradient_background(1024, 1024, (45, 90, 45), (26, 58, 26))
    draw = ImageDraw.Draw(img)
    
    # 金色外环
    draw_golden_ring(draw, (512, 512), 500, 420)
    
    # 图腾柱
    for y in range(250, 800):
        brightness = int(139 - (y - 250) * 0.15)
        draw.rectangle([(462, y), (562, y + 1)], fill=(brightness, min(80, brightness // 2), min(50, brightness // 3)))
    
    # 头骨
    draw.ellipse([(432, 270), (592, 430)], fill=(212, 197, 163))
    
    # 眼窝
    draw.ellipse([(460, 315), (510, 365)], fill=(26, 26, 26))
    draw.ellipse([(514, 315), (564, 365)], fill=(26, 26, 26))
    
    # 獠牙
    tooth_points_l = [(490, 390), (480, 440), (500, 410)]
    tooth_points_r = [(534, 390), (544, 440), (524, 410)]
    draw.polygon(tooth_points_l, fill=(240, 224, 208))
    draw.polygon(tooth_points_r, fill=(240, 224, 208))
    
    # 装饰条纹
    draw.rectangle([(462, 500), (562, 510)], fill=(255, 69, 0))
    draw.rectangle([(462, 600), (562, 610)], fill=(255, 69, 0))
    
    # 绿色光晕
    for r in range(120, 100, -3):
        draw.ellipse([(512-r, 350-r), (512+r, 350+r)], outline=(0, 255, 0, 76))
    
    return img

def draw_dark_fortress():
    """5. 黑暗要塞 - 坚固堡垒"""
    img = create_gradient_background(1024, 1024, (26, 42, 58), (10, 26, 42))
    draw = ImageDraw.Draw(img)
    
    # 银色外环
    draw_silver_ring(draw, (512, 512), 500, 420)
    
    # 要塞主体
    for y in range(450, 800):
        brightness = int(74 - (y - 450) * 0.08)
        draw.rectangle([(300, y), (724, y + 1)], fill=(brightness, min(100, brightness + 26), min(120, brightness + 46)))
    
    # 城墙垛口
    for i in range(7):
        draw.rectangle([(320 + i * 60, 400), (360 + i * 60, 450)], fill=(58, 74, 90))
    
    # 中央塔楼
    draw.rectangle([(420, 300), (604, 450)], fill=(90, 106, 122))
    tower_top = [(400, 300), (512, 220), (624, 300)]
    draw.polygon(tower_top, fill=(90, 106, 122))
    
    # 窗户光芒
    window_positions = [(480, 500), (514, 500), (480, 600), (514, 600)]
    for wx, wy in window_positions:
        draw.rectangle([(wx, wy), (wx + 30, wy + 50)], fill=(255, 215, 0))
    
    # 大门
    draw.rectangle([(442, 730), (582, 800)], fill=(26, 42, 58))
    draw.arc([(442, 730), (582, 870)], 0, 180, fill=(26, 42, 58), width=70)
    
    return img

def draw_dragon_lair():
    """6. 龙之巢穴 - 龙影"""
    img = create_gradient_background(1024, 1024, (74, 26, 26), (42, 10, 10))
    draw = ImageDraw.Draw(img)
    
    # 金色外环
    draw_golden_ring(draw, (512, 512), 500, 420)
    
    # 龙身体曲线
    points = []
    for t in range(0, 101, 2):
        t_norm = t / 100
        x = 300 + 424 * t_norm
        y = 600 - 100 * math.sin(t_norm * math.pi) + 50 * math.sin(t_norm * 3 * math.pi)
        points.append((x, y))
    
    # 绘制龙身（外层）
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(139, 0, 0), width=60)
    
    # 龙身高光
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(205, 0, 0), width=40)
    
    # 龙头
    draw.ellipse([(660, 440), (788, 520)], fill=(139, 0, 0))
    
    # 龙角
    horn_l = [(700, 440), (680, 360), (720, 430)]
    horn_r = [(740, 450), (760, 370), (730, 445)]
    draw.polygon(horn_l, fill=(255, 215, 0))
    draw.polygon(horn_r, fill=(255, 215, 0))
    
    # 龙眼睛（发光）
    draw.ellipse([(735, 465), (755, 485)], fill=(255, 255, 0))
    
    # 火焰效果
    for r in range(120, 0, -5):
        color_val = int(255 * (r / 120))
        alpha = int(150 * (r / 120))
        draw.ellipse([(780-r, 450-r), (780+r, 450+r)], fill=(255, color_val, 0, alpha))
    
    return img

def draw_demon_throne():
    """7. 恶魔王座 - 王座、恶魔符号"""
    img = create_gradient_background(1024, 1024, (58, 26, 58), (42, 10, 42))
    draw = ImageDraw.Draw(img)
    
    # 金色外环
    draw_golden_ring(draw, (512, 512), 500, 420)
    
    # 王座主体
    for y in range(400, 800):
        brightness = int(74 - (y - 400) * 0.1)
        draw.rectangle([(380, y), (644, y + 1)], fill=(brightness, min(40, brightness // 3), brightness))
    
    # 王座靠背
    back_points = [(380, 400), (350, 250), (420, 300), (512, 280), (604, 300), (674, 250), (644, 400)]
    draw.polygon(back_points, fill=(74, 26, 74))
    
    # 王座装饰金边
    draw.rectangle([(390, 420), (634, 780)], outline=(255, 215, 0), width=8)
    
    # 恶魔符号（倒五角星）
    star_points = []
    star_cx, star_cy, star_r = 512, 550, 80
    for i in range(5):
        angle = (i * 4 * math.pi / 5) - math.pi / 2
        x = star_cx + int(star_r * math.cos(angle))
        y = star_cy + int(star_r * math.sin(angle))
        star_points.append((x, y))
    
    # 绘制五角星
    for i in range(5):
        draw.line([star_points[i], star_points[(i + 2) % 5]], fill=(255, 0, 0), width=8)
    
    # 紫色光晕
    for r in range(120, 80, -5):
        draw.ellipse([(512-r, 600-r), (512+r, 600+r)], outline=(139, 0, 139, 100))
    
    return img

def draw_void_temple():
    """8. 虚空神殿 - 神秘神殿、紫色能量"""
    img = create_gradient_background(1024, 1024, (42, 26, 74), (26, 10, 58))
    draw = ImageDraw.Draw(img)
    
    # 银色外环
    draw_silver_ring(draw, (512, 512), 500, 420)
    
    # 神殿主体
    for y in range(400, 750):
        brightness = int(106 - (y - 400) * 0.1)
        draw.rectangle([(380, y), (644, y + 1)], fill=(brightness, min(80, brightness - 26), min(160, brightness + 54)))
    
    # 柱子
    for i in range(5):
        x = 400 + i * 60
        draw.rectangle([(x, 400), (x + 30, 750)], fill=(122, 90, 154))
        draw.rectangle([(x - 10, 380), (x + 40, 400)], fill=(154, 122, 186))
    
    # 三角形屋顶
    roof_points = [(350, 400), (512, 250), (674, 400)]
    draw.polygon(roof_points, fill=(138, 106, 170))
    
    # 紫色能量球
    for r in range(120, 0, -3):
        inner = int(224 * (r / 120))
        draw.ellipse([(512-r, 550-r), (512+r, 550+r)], fill=(inner, min(200, inner - 60), 255, int(150 * r / 120)))
    
    # 能量光束
    for i in range(8):
        angle = (i / 8) * math.pi * 2
        x1 = 512 + int(100 * math.cos(angle))
        y1 = 550 + int(100 * math.sin(angle))
        x2 = 512 + int(180 * math.cos(angle))
        y2 = 550 + int(180 * math.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=(139, 0, 255, 128), width=5)
    
    return img

def main():
    """主函数：生成所有图标"""
    icons = [
        ("border_outpost.png", "边境哨站", draw_border_outpost),
        ("bandit_camp.png", "强盗营地", draw_bandit_camp),
        ("abandoned_castle.png", "废弃城堡", draw_abandoned_castle),
        ("orc_tribe.png", "兽人部落", draw_orc_tribe),
        ("dark_fortress.png", "黑暗要塞", draw_dark_fortress),
        ("dragon_lair.png", "龙之巢穴", draw_dragon_lair),
        ("demon_throne.png", "恶魔王座", draw_demon_throne),
        ("void_temple.png", "虚空神殿", draw_void_temple),
    ]
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for filename, name, draw_func in icons:
        print(f"正在生成：{name} ({filename})")
        img = draw_func()
        filepath = os.path.join(OUTPUT_DIR, filename)
        img.save(filepath, "PNG")
        print(f"  已保存到：{filepath}")
    
    print("\n所有图标生成完成！")

if __name__ == "__main__":
    main()

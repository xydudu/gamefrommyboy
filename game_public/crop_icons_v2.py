#!/usr/bin/env python3
from PIL import Image
import os

# 读取截图
img = Image.open('/root/.openclaw/media/inbound/8c71be61-3720-42ad-b474-4a96982781e4.jpg')
width, height = img.size
print(f"原图尺寸：{width}x{height}")

# 根据截图重新计算图标位置（更精确的坐标）
# 从截图看，图标在卡片上部，需要更精确的裁剪
icon_positions = [
    # 边境哨站 (左上)
    (80, 320, 280, 520),
    # 强盗营地 (右上)
    (760, 320, 960, 520),
    # 废弃城堡 (左 2)
    (80, 670, 280, 870),
    # 兽人部落 (右 2)
    (760, 670, 960, 870),
    # 黑暗要塞 (左 3)
    (80, 1020, 280, 1220),
    # 龙之巢穴 (右 3)
    (760, 1020, 960, 1220),
    # 恶魔王座 (左下)
    (80, 1370, 280, 1570),
    # 虚空神殿 (右下)
    (760, 1370, 960, 1570)
]

target_names = [
    'border_outpost',   # 边境哨站
    'bandit_camp',      # 强盗营地
    'abandoned_castle', # 废弃城堡
    'orc_tribe',        # 兽人部落
    'dark_fortress',    # 黑暗要塞
    'dragon_lair',      # 龙之巢穴
    'demon_throne',     # 恶魔王座
    'void_temple'       # 虚空神殿
]

# 创建 icons 目录
os.makedirs('/root/.openclaw/workspace/game_public/icons', exist_ok=True)

def remove_background(icon_img):
    """移除深色背景，保留图标主体"""
    icon_img = icon_img.convert("RGBA")
    datas = icon_img.getdata()
    
    new_data = []
    for item in datas:
        # 深色背景变透明（RGB 值都低于 80 的像素）
        if item[0] < 80 and item[1] < 80 and item[2] < 80:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    icon_img.putdata(new_data)
    return icon_img

# 裁剪并保存每个图标
for i, (pos, name) in enumerate(zip(icon_positions, target_names)):
    icon = img.crop(pos)
    # 移除背景
    icon = remove_background(icon)
    output_path = f'/root/.openclaw/workspace/game_public/icons/{name}.png'
    icon.save(output_path, 'PNG')
    print(f"已保存：{output_path}")

print("\n完成！共处理 8 个图标，背景已透明化。")

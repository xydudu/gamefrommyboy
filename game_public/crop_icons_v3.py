#!/usr/bin/env python3
from PIL import Image
import os

# 读取截图
img = Image.open('/root/.openclaw/media/inbound/8c71be61-3720-42ad-b474-4a96982781e4.jpg')
width, height = img.size
print(f"原图尺寸：{width}x{height}")

# 重新调整裁剪区域，扩大范围确保图标完整
icon_positions = [
    # 边境哨站 (左上) - 扩大范围
    (40, 250, 320, 600),
    # 强盗营地 (右上)
    (720, 250, 1000, 600),
    # 废弃城堡 (左 2)
    (40, 600, 320, 950),
    # 兽人部落 (右 2)
    (720, 600, 1000, 950),
    # 黑暗要塞 (左 3)
    (40, 950, 320, 1300),
    # 龙之巢穴 (右 3)
    (720, 950, 1000, 1300),
    # 恶魔王座 (左下)
    (40, 1300, 320, 1650),
    # 虚空神殿 (右下)
    (720, 1300, 1000, 1650)
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
        # 深色背景变透明（RGB 值都低于 100 的像素）
        if item[0] < 100 and item[1] < 100 and item[2] < 100:
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
    print(f"已保存：{output_path} - 尺寸：{icon.size}")

print("\n完成！共处理 8 个图标。")

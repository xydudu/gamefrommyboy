#!/usr/bin/env python3
from PIL import Image
import os

# 读取截图
img = Image.open('/root/.openclaw/media/inbound/8c71be61-3720-42ad-b474-4a96982781e4.jpg')
width, height = img.size
print(f"原图尺寸：{width}x{height}")

# 根据截图布局计算图标位置（2 列 4 行）
# 估算每个卡片的位置
card_width = width // 2
card_height = height // 4

# 图标在卡片中的大致位置（需要根据实际截图调整）
# 从截图看，图标在卡片上部中央
icon_positions = [
    # (x_start, y_start, x_end, y_end) - 根据截图估算
    (50, 280, 350, 580),    # 边境哨站 (左上)
    (730, 280, 1030, 580),  # 强盗营地 (右上)
    (50, 630, 350, 930),    # 废弃城堡 (左 2)
    (730, 630, 1030, 930),  # 兽人部落 (右 2)
    (50, 980, 350, 1280),   # 黑暗要塞 (左 3)
    (730, 980, 1030, 1280), # 龙之巢穴 (右 3)
    (50, 1330, 350, 1630),  # 恶魔王座 (左下)
    (730, 1330, 1030, 1630) # 虚空神殿 (右下)
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

# 裁剪并保存每个图标
for i, (pos, name) in enumerate(zip(icon_positions, target_names)):
    icon = img.crop(pos)
    output_path = f'/root/.openclaw/workspace/game_public/icons/{name}.png'
    icon.save(output_path)
    print(f"已保存：{output_path} ({pos})")

print("\n完成！共裁剪 8 个图标。")

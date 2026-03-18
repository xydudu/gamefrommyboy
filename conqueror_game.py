"""
征服者游戏 - Python/Pygame
20个不规则国家，6种兵种，回合制战斗，射程系统
"""

import pygame
import random
import math

pygame.init()

# 窗口设置
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("征服者")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
CYAN = (0, 206, 209)

# 字体
try:
    font_large = pygame.font.SysFont("simhei", 48)
    font_medium = pygame.font.SysFont("simhei", 28)
    font_small = pygame.font.SysFont("simhei", 20)
except:
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 20)

# 游戏状态
STATE_MENU = "menu"
STATE_MAP = "map"
STATE_RECRUIT = "recruit"
STATE_BATTLE = "battle"
STATE_DEFENSE = "defense"
STATE_RESULT = "result"
STATE_UNLOCK = "unlock"
STATE_UPGRADE = "upgrade"

current_state = STATE_MENU

# 兵种基础数据
UNIT_BASE = {
    "步兵": {"cost": 50, "attack": 20, "hp": 40, "range": 1, "color": GREEN},
    "弓兵": {"cost": 100, "attack": 20, "hp": 30, "range": 1, "color": BLUE},
    "盾兵": {"cost": 150, "attack": 20, "hp": 50, "range": 1, "color": GRAY},
    "矛兵": {"cost": 150, "attack": 60, "hp": 60, "range": 1, "color": BROWN},
    "枪兵": {"cost": 200, "attack": 60, "hp": 60, "range": 2, "color": PURPLE},
    "坦克": {"cost": 250, "attack": 80, "hp": 100, "range": 3, "color": DARK_GRAY},
}

# 升级后属性
UNIT_LEVELS = {
    "步兵": [
        {"attack": 20, "hp": 40},
        {"attack": 40, "hp": 60},
        {"attack": 70, "hp": 80},
        {"attack": 90, "hp": 100},
    ],
    "弓兵": [
        {"attack": 20, "hp": 30, "range": 1},
        {"attack": 40, "hp": 60, "range": 2},
        {"attack": 50, "hp": 80, "range": 3},
        {"attack": 60, "hp": 100, "range": 4},
    ],
    "盾兵": [
        {"attack": 20, "hp": 50},
        {"attack": 40, "hp": 100},
        {"attack": 60, "hp": 120},
        {"attack": 100, "hp": 200},
    ],
    "矛兵": [
        {"attack": 60, "hp": 60},
        {"attack": 80, "hp": 70},
        {"attack": 100, "hp": 80},
        {"attack": 150, "hp": 120},
    ],
    "枪兵": [
        {"attack": 60, "hp": 60, "range": 2},
        {"attack": 80, "hp": 80, "range": 3},
        {"attack": 100, "hp": 100, "range": 4},
        {"attack": 100, "hp": 100, "range": 4},
    ],
    "坦克": [
        {"attack": 80, "hp": 100, "range": 3},
        {"attack": 100, "hp": 150, "range": 4},
        {"attack": 120, "hp": 200, "range": 5},
        {"attack": 180, "hp": 200, "range": 6},
    ],
}

# 升级费用
UPGRADE_COST = {
    "步兵": [250, 500, 750],
    "弓兵": [350, 700, 1050],
    "盾兵": [400, 800, 1200],
    "矛兵": [450, 900, 1350],
    "枪兵": [450, 900, 1350],
    "坦克": [500, 1000, 1500],
}

# 解锁费用
UNLOCK_COST = {
    "盾兵": 200,
    "矛兵": 200,
    "枪兵": 250,
    "坦克": 300,
}

# 玩家数据
player_money = 500
owned_territories = [0]

# 兵种库存
player_units = {
    "步兵": [1, 1, 1, 1, 1],
    "弓兵": [1, 1, 1],
    "盾兵": [],
    "矛兵": [],
    "枪兵": [],
    "坦克": [],
}

# 解锁状态
unlocked_units = {"步兵": True, "弓兵": True, "盾兵": False, "矛兵": False, "枪兵": False, "坦克": False}

# 当前选中的国家
current_target = None

# 战斗相关
battle_result = None
defense_timer = 0
can_attack_again = False
last_battle_units = None
reward_money = 0
battle_log = []

# 国家类
class Country:
    def __init__(self, id, name, x, y, points, color):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.points = points
        self.color = color
        self.owner = None
        self.tax = random.randint(50, 150)
        self.defense_units = self._generate_defense()
        
    def _generate_defense(self):
        units = {}
        difficulty = random.randint(3, 8)
        available = ["步兵", "弓兵", "盾兵", "矛兵"]
        if random.random() > 0.5:
            available.append("枪兵")
        if random.random() > 0.7:
            available.append("坦克")
        for _ in range(difficulty):
            unit = random.choice(available)
            level = random.randint(1, min(3, 1 + self.id // 7))
            if unit not in units:
                units[unit] = []
            units[unit].append(level)
        return units
    
    def draw(self, surface):
        color = self.color if self.owner is None else (GREEN if self.owner == 0 else RED)
        pygame.draw.polygon(surface, color, self.points)
        pygame.draw.polygon(surface, BLACK, self.points, 2)
        text = font_small.render(self.name, True, BLACK)
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)
        tax_text = font_small.render(f"税:{self.tax}", True, BLACK)
        surface.blit(tax_text, (self.x - 25, self.y + 15))

def generate_countries():
    countries = []
    names = ["北风国", "南疆国", "东海国", "西域国", "中原国", 
             "云山国", "林海国", "雪原国", "沙漠国", "沼泽国",
             "峡谷国", "平原国", "高原国", "半岛国", "岛国",
             "草原国", "矿脉国", "渔港国", "商贸国", "边陲国"]
    colors = [(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)) for _ in range(20)]
    positions = [
        (150, 150), (350, 120), (550, 150), (750, 130), (950, 160),
        (200, 300), (400, 280), (600, 320), (800, 290), (1000, 310),
        (180, 450), (380, 430), (580, 470), (780, 440), (980, 460),
        (250, 600), (450, 580), (650, 620), (850, 590), (1050, 610),
    ]
    for i, (name, pos, color) in enumerate(zip(names, positions, colors)):
        points = []
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            radius = random.randint(40, 70)
            px = pos[0] + math.cos(rad) * radius
            py = pos[1] + math.sin(rad) * radius
            points.append((px, py))
        country = Country(i, name, pos[0], pos[1], points, color)
        if i == 0:
            country.owner = 0
        countries.append(country)
    return countries

countries = generate_countries()

# 按钮类
class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, enabled=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.enabled = enabled
        
    def draw(self, surface):
        if not self.enabled:
            color = DARK_GRAY
        elif self.hover:
            color = LIGHT_GRAY
        else:
            color = self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text = font_medium.render(self.text, True, BLACK if self.enabled else GRAY)
        rect = text.get_rect(center=self.rect.center)
        surface.blit(text, rect)
        
    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)

# 按钮定义
start_button = Button(500, 400, 200, 60, "开始游戏", GREEN)
back_button = Button(20, 20, 100, 40, "返回")
attack_button = Button(500, 720, 200, 60, "进攻", RED)
defense_button = Button(500, 400, 200, 80, "防守战", RED)
attack_again_button = Button(500, 500, 200, 60, "进攻", ORANGE)
unlock_button = Button(450, 600, 300, 50, "解锁新兵种", YELLOW)
upgrade_button = Button(450, 660, 300, 50, "升级兵种", CYAN)
auto_battle_button = Button(500, 700, 200, 60, "自动战斗", BLUE)

# 购买按钮
buy_buttons = {}
for i, name in enumerate(UNIT_BASE.keys()):
    x = 150 + (i % 3) * 350
    y = 280 + (i // 3) * 140
    buy_buttons[name] = Button(x, y + 80, 150, 50, f"购买", GREEN)

# 解锁按钮
unlock_buttons = {}
for i, (name, cost) in enumerate(UNLOCK_COST.items()):
    unlock_buttons[name] = Button(300 + (i % 2) * 400, 250 + (i // 2) * 120, 300, 80, 
                                   f"解锁{name}\n需要{cost}元", YELLOW)

# 升级按钮
upgrade_buttons = {}
for i, name in enumerate(UNIT_BASE.keys()):
    upgrade_buttons[name] = Button(200 + (i % 3) * 350, 200 + (i // 3) * 160, 280, 120, 
                                    f"{name}\n查看升级", CYAN)

def get_unit_stats(name, level):
    base = UNIT_BASE[name]
    if name in UNIT_LEVELS and level <= len(UNIT_LEVELS[name]):
        stats = UNIT_LEVELS[name][level - 1]
        return {"attack": stats["attack"], "hp": stats["hp"], "range": stats.get("range", base.get("range", 1))}
    return {"attack": base["attack"], "hp": base["hp"], "range": base.get("range", 1)}

def flatten_units(units_dict):
    result = []
    for name, levels in units_dict.items():
        for level in levels:
            stats = get_unit_stats(name, level)
            result.append({"name": name, "level": level, "max_hp": stats["hp"], "hp": stats["hp"], 
                          "attack": stats["attack"], "range": stats["range"]})
    return result

def simulate_turn_battle(attacker_units_dict, defender_units_dict, max_turns=50):
    global battle_log
    battle_log = []
    
    attackers = flatten_units(attacker_units_dict)
    defenders = flatten_units(defender_units_dict)
    
    if not attackers:
        return "lose", []
    if not defenders:
        return "win", attackers
    
    for turn in range(max_turns):
        # 我方回合
        for unit in attackers[:]:
            if unit["hp"] <= 0:
                continue
            if not defenders:
                break
            target = defenders[0] if defenders else None
            if target:
                damage = unit["attack"]
                target["hp"] -= damage
                battle_log.append(f"我方{unit['name']}Lv{unit['level']} 攻击 敌方{target['name']}Lv{target['level']} 造成{damage}伤")
                if target["hp"] <= 0:
                    battle_log.append(f"  -> 敌方{target['name']}Lv{target['level']} 被击败!")
                    defenders.remove(target)
        
        if not defenders:
            return "win", attackers
        
        # 敌方回合
        for unit in defenders[:]:
            if unit["hp"] <= 0:
                continue
            if not attackers:
                break
            target = attackers[0] if attackers else None
            if target:
                damage = unit["attack"]
                target["hp"] -= damage
                battle_log.append(f"敌方{unit['name']}Lv{unit['level']} 攻击 我方{target['name']}Lv{target['level']} 造成{damage}伤")
                if target["hp"] <= 0:
                    battle_log.append(f"  -> 我方{target['name']}Lv{target['level']} 被击败!")
                    attackers.remove(target)
        
        if not attackers:
            return "lose", defenders
    
    attacker_power = sum(u["hp"] for u in attackers)
    defender_power = sum(u["hp"] for u in defenders)
    if attacker_power > defender_power:
        return "win", attackers
    elif attacker_power == defender_power:
        return "draw", []
    else:
        return "lose", defenders

def count_units_by_level(name):
    levels = player_units.get(name, [])
    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for lvl in levels:
        counts[lvl] = counts.get(lvl, 0) + 1
    return counts

def draw_menu():
    screen.fill(WHITE)
    title = font_large.render("征服者", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//2 - 80, 200))
    subtitle = font_medium.render("点击开始征服世界", True, GRAY)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - 120, 300))
    start_button.draw(screen)

def draw_map():
    screen.fill(WHITE)
    title = font_medium.render(f"选择目标国家 | 金钱: {player_money} | 领土: {len(owned_territories)}", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//2 - 200, 20))
    for country in countries:
        country.draw(screen)
    back_button.draw(screen)

def draw_recruit():
    screen.fill(WHITE)
    if current_target is not None:
        target = countries[current_target]
        title = font_large.render(f"攻打 {target.name}", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - 100, 70))
        
        enemy_text = font_medium.render("敌方兵力:", True, RED)
        screen.blit(enemy_text, (50, 130))
        y = 165
        for unit, levels in target.defense_units.items():
            level_str = ",".join([f"{l}级" for l in sorted(levels)])
            text = font_small.render(f"{unit}: {level_str}", True, BLACK)
            screen.blit(text, (50, y))
            y += 25
        
        my_text = font_medium.render("我方兵力:", True, GREEN)
        screen.blit(my_text, (350, 130))
        y = 165
        for name, levels in player_units.items():
            if levels:
                counts = count_units_by_level(name)
                parts = [f"{lvl}级x{c}" for lvl, c in counts.items() if c > 0]
                text = font_small.render(f"{name}: {', '.join(parts)}", True, BLACK)
                screen.blit(text, (350, y))
                y += 25
        
        buy_text = font_medium.render(f"购买新兵 (金钱: {player_money})", True, BLACK)
        screen.blit(buy_text, (SCREEN_WIDTH//2 - 150, 240))
        
        for i, (name, data) in enumerate(UNIT_BASE.items()):
            x = 150 + (i % 3) * 350
            y = 280 + (i // 3) * 140
            pygame.draw.rect(screen, LIGHT_GRAY, (x - 10, y - 10, 330, 130))
            pygame.draw.rect(screen, BLACK, (x - 10, y - 10, 330, 130), 1)
            color = data["color"] if unlocked_units[name] else GRAY
            name_text = font_medium.render(name, True, color)
            screen.blit(name_text, (x, y))
            if unlocked_units[name]:
                stats = get_unit_stats(name, 1)
                info_text = font_small.render(f"价格:{data['cost']} 攻:{stats['attack']} 血:{stats['hp']} 射程:{stats['range']}", True, BLACK)
                screen.blit(info_text, (x, y + 30))
                counts = count_units_by_level(name)
                total = sum(counts.values())
                if total > 0:
                    parts = [f"{lvl}级x{c}" for lvl, c in counts.items() if c > 0]
                    own_text = font_small.render(f"拥有: {', '.join(parts)}", True, BLUE)
                    screen.blit(own_text, (x, y + 55))
                buy_buttons[name].enabled = player_money >= data["cost"]
                buy_buttons[name].rect.topleft = (x, y + 80)
                buy_buttons[name].draw(screen)
            else:
                lock_text = font_small.render(f"[未解锁] 解锁需{UNLOCK_COST[name]}元", True, RED)
                screen.blit(lock_text, (x, y + 35))
        
        unlock_button.enabled = True
        unlock_button.draw(screen)
        upgrade_button.enabled = True
        upgrade_button.draw(screen)
    
    back_button.draw(screen)
    attack_button.enabled = any(player_units.values())
    attack_button.draw(screen)

def draw_unlock():
    screen.fill(WHITE)
    title = font_large.render("解锁新兵种", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//2 - 100, 80))
    info = font_medium.render(f"当前金钱: {player_money}", True, BLACK)
    screen.blit(info, (SCREEN_WIDTH//2 - 80, 140))
    for name, btn in unlock_buttons.items():
        if not unlocked_units[name]:
            btn.enabled = player_money >= UNLOCK_COST[name]
            btn.draw(screen)
        else:
            text = font_medium.render(f"{name} - 已解锁", True, GREEN)
            screen.blit(text, (btn.rect.x + 50, btn.rect.y + 25))
    back_button.draw(screen)

def draw_upgrade():
    screen.fill(WHITE)
    title = font_large.render("升级兵种", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//2 - 100, 60))
    info = font_medium.render(f"当前金钱: {player_money}", True, BLACK)
    screen.blit(info, (SCREEN_WIDTH//2 - 80, 110))
    for i, (name, btn) in enumerate(upgrade_buttons.items()):
        x = 200 + (i % 3) * 350
        y = 160 + (i // 3) * 160
        pygame.draw.rect(screen, LIGHT_GRAY, (x - 10, y - 10, 320, 140))
        counts = count_units_by_level(name)
        total = sum(counts.values())
        name_text = font_medium.render(name, True, UNIT_BASE[name]["color"])
        screen.blit(name_text, (x, y))
        if total > 0:
            y_offset = 35
            for lvl in [1, 2, 3, 4]:
                if counts[lvl] > 0:
                    stats = get_unit_stats(name, lvl)
                    text = font_small.render(f"{lvl}级x{counts[lvl]}: 攻{stats['attack']} 血{stats['hp']}", True, BLACK)
                    screen.blit(text, (x, y + y_offset))
                    y_offset += 22
            can_upgrade = any(lvl < 4 and counts[lvl] > 0 for lvl in [1, 2, 3])
            if can_upgrade:
                for lvl in [1, 2, 3]:
                    if counts[lvl] > 0:
                        cost = UPGRADE_COST[name][lvl - 1]
                        upgrade_btn = Button(x + 80, y + 110, 140, 30, f"升{lvl+1}级 ({cost}元)", YELLOW, player_money >= cost)
                        upgrade_btn.draw(screen)
                        break
        else:
            text = font_small.render("未拥有该兵种", True, GRAY)
            screen.blit(text, (x, y + 40))
    back_button.draw(screen)

def draw_battle():
    screen.fill(WHITE)
    if battle_result is None:
        title = font_large.render("战斗中...", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - 80, 50))
        y = 120
        for log in battle_log[-20:]:
            text = font_small.render(log, True, BLACK)
            screen.blit(text, (50, y))
            y += 22
        auto_battle_button.draw(screen)
    else:
        if battle_result == "win":
            result_text = font_large.render("胜利！", True, GREEN)
        elif battle_result == "draw":
            result_text = font_large.render("平局", True, YELLOW)
        else:
            result_text = font_large.render("失败！", True, RED)
        screen.blit(result_text, (SCREEN_WIDTH//2 - 60, 300))
        back_button.rect.topleft = (550, 450)
        back_button.draw(screen)

def draw_defense():
    screen.fill(WHITE)
    title = font_large.render("防守战", True, RED)
    screen.blit(title, (SCREEN_WIDTH//2 - 80, 100))
    enemy_text = font_medium.render("敌方进攻兵力:", True, RED)
    screen.blit(enemy_text, (100, 180))
    if last_battle_units:
        y = 220
        for unit, levels in last_battle_units.items():
            counts = {}
            for lvl in levels:
                counts[lvl] = counts.get(lvl, 0) + 1
            parts = [f"{lvl}级x{c}" for lvl, c in sorted(counts.items())]
            text = font_small.render(f"{unit}: {', '.join(parts)}", True, BLACK)
            screen.blit(text, (100, y))
            y += 28
    my_text = font_medium.render("我方防守兵力:", True, GREEN)
    screen.blit(my_text, (450, 180))
    y = 220
    for name, levels in player_units.items():
        if levels:
            counts = count_units_by_level(name)
            parts = [f"{lvl}级x{c}" for lvl, c in counts.items() if c > 0]
            text = font_small.render(f"{name}: {', '.join(parts)}", True, BLACK)
            screen.blit(text, (450, y))
            y += 28
    defense_button.draw(screen)

def draw_result():
    screen.fill(WHITE)
    if battle_result == "win_defense":
        title = font_large.render("防守胜利！", True, GREEN)
        screen.blit(title, (SCREEN_WIDTH//2 - 100, 150))
        msg = font_medium.render(f"获得 {reward_money} 元和半块地！", True, BLACK)
        screen.blit(msg, (SCREEN_WIDTH//2 - 150, 250))
        if can_attack_again:
            elapsed = (pygame.time.get_ticks() - defense_timer) / 1000
            remaining = max(0, 5 - elapsed)
            timer_text = font_medium.render(f"{remaining:.1f}秒内可再次进攻", True, ORANGE)
            screen.blit(timer_text, (SCREEN_WIDTH//2 - 150, 350))
            attack_again_button.draw(screen)
        else:
            timeout_text = font_medium.render("进攻时机已错过，返回地图", True, GRAY)
            screen.blit(timeout_text, (SCREEN_WIDTH//2 - 150, 350))
            back_button.draw(screen)
    else:
        title = font_large.render("防守失败...", True, RED)
        screen.blit(title, (SCREEN_WIDTH//2 - 100, 300))
        back_button.draw(screen)

# 主循环
running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEMOTION:
            for btn in [start_button, back_button, attack_button, defense_button, 
                       attack_again_button, unlock_button, upgrade_button, auto_battle_button]:
                btn.hover = btn.is_clicked(mouse_pos)
            for btn in buy_buttons.values():
                btn.hover = btn.is_clicked(mouse_pos)
            for btn in unlock_buttons.values():
                btn.hover = btn.is_clicked(mouse_pos)
            for btn in upgrade_buttons.values():
                btn.hover = btn.is_clicked(mouse_pos)
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == STATE_MENU:
                if start_button.is_clicked(mouse_pos):
                    current_state = STATE_MAP
                    
            elif current_state == STATE_MAP:
                if back_button.is_clicked(mouse_pos):
                    running = False
                else:
                    for country in countries:
                        if country.owner != 0:
                            dx = mouse_pos[0] - country.x
                            dy = mouse_pos[1] - country.y
                            if math.sqrt(dx*dx + dy*dy) < 50:
                                current_target = country.id
                                current_state = STATE_RECRUIT
                                break
                                
            elif current_state == STATE_RECRUIT:
                if back_button.is_clicked(mouse_pos):
                    current_state = STATE_MAP
                    current_target = None
                elif unlock_button.is_clicked(mouse_pos):
                    current_state = STATE_UNLOCK
                elif upgrade_button.is_clicked(mouse_pos):
                    current_state = STATE_UPGRADE
                elif attack_button.is_clicked(mouse_pos):
                    if current_target is not None:
                        target = countries[current_target]
                        battle_result, survivors = simulate_turn_battle(player_units, target.defense_units)
                        current_state = STATE_BATTLE
                        if battle_result == "win":
                            reward_money = random.randint(500, 1000)
                            player_money += reward_money + target.tax
                            target.owner = 0
                            if target.id not in owned_territories:
                                owned_territories.append(target.id)
                        elif battle_result == "lose":
                            last_battle_units = {k: v[:] for k, v in target.defense_units.items()}
                else:
                    for name, btn in buy_buttons.items():
                        if btn.is_clicked(mouse_pos) and unlocked_units[name]:
                            cost = UNIT_BASE[name]["cost"]
                            if player_money >= cost:
                                player_money -= cost
                                player_units[name].append(1)
                                
            elif current_state == STATE_UNLOCK:
                if back_button.is_clicked(mouse_pos):
                    current_state = STATE_RECRUIT
                else:
                    for name, btn in unlock_buttons.items():
                        if btn.is_clicked(mouse_pos) and not unlocked_units[name]:
                            cost = UNLOCK_COST[name]
                            if player_money >= cost:
                                player_money -= cost
                                unlocked_units[name] = True
                                
            elif current_state == STATE_UPGRADE:
                if back_button.is_clicked(mouse_pos):
                    current_state = STATE_RECRUIT
                else:
                    for name, btn in upgrade_buttons.items():
                        if btn.rect.collidepoint(mouse_pos):
                            counts = count_units_by_level(name)
                            for lvl in [1, 2, 3]:
                                if counts[lvl] > 0:
                                    cost = UPGRADE_COST[name][lvl - 1]
                                    if player_money >= cost:
                                        player_money -= cost
                                        for i, unit_lvl in enumerate(player_units[name]):
                                            if unit_lvl == lvl:
                                                player_units[name][i] = lvl + 1
                                                break
                                    break
                            
            elif current_state == STATE_BATTLE:
                if battle_result is None:
                    if auto_battle_button.is_clicked(mouse_pos):
                        target = countries[current_target]
                        battle_result, survivors = simulate_turn_battle(player_units, target.defense_units)
                        if battle_result == "win":
                            reward_money = random.randint(500, 1000)
                            player_money += reward_money + target.tax
                            target.owner = 0
                            if target.id not in owned_territories:
                                owned_territories.append(target.id)
                        elif battle_result == "lose":
                            last_battle_units = {k: v[:] for k, v in target.defense_units.items()}
                else:
                    if back_button.is_clicked(mouse_pos):
                        if battle_result == "win" or battle_result == "draw":
                            current_state = STATE_MAP
                        else:
                            current_state = STATE_DEFENSE
                        battle_result = None
                        
            elif current_state == STATE_DEFENSE:
                if defense_button.is_clicked(mouse_pos):
                    if last_battle_units:
                        defense_result, survivors = simulate_turn_battle(player_units, last_battle_units)
                        if defense_result in ["win", "draw"]:
                            battle_result = "win_defense"
                            reward_money = random.randint(200, 500)
                            player_money += reward_money
                            if current_target is not None:
                                countries[current_target].tax //= 2
                            can_attack_again = True
                            defense_timer = pygame.time.get_ticks()
                        else:
                            battle_result = "lose_defense"
                            can_attack_again = False
                        current_state = STATE_RESULT
                        
            elif current_state == STATE_RESULT:
                if back_button.is_clicked(mouse_pos):
                    current_state = STATE_MAP
                    current_target = None
                    battle_result = None
                elif attack_again_button.is_clicked(mouse_pos) and can_attack_again:
                    current_state = STATE_RECRUIT
                    battle_result = None
    
    if current_state == STATE_RESULT and can_attack_again:
        elapsed = (pygame.time.get_ticks() - defense_timer) / 1000
        if elapsed >= 5:
            can_attack_again = False
    
    if current_state == STATE_MENU:
        draw_menu()
    elif current_state == STATE_MAP:
        draw_map()
    elif current_state == STATE_RECRUIT:
        draw_recruit()
    elif current_state == STATE_UNLOCK:
        draw_unlock()
    elif current_state == STATE_UPGRADE:
        draw_upgrade()
    elif current_state == STATE_BATTLE:
        draw_battle()
    elif current_state == STATE_DEFENSE:
        draw_defense()
    elif current_state == STATE_RESULT:
        draw_result()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

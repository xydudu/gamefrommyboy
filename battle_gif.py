import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import random
import math

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 颜色定义
RED = '#FF4444'
BLUE = '#4444FF'
GREEN = '#44AA44'
YELLOW = '#FFAA00'
GRAY = '#888888'
DARK_GRAY = '#444444'
BLACK = '#000000'
WHITE = '#FFFFFF'
GROUND_Y = 0.3

class StickMan:
    def __init__(self, x, y, team, unit_type):
        self.x = x
        self.y = y
        self.team = team
        self.unit_type = unit_type
        self.alive = True
        self.direction = 1 if team == 'red' else -1
        self.set_unit_stats()
        
        self.anim_frame = 0
        self.state = 'idle'
        self.attack_cooldown = 0
        self.target = None
        self.effects = []
        
    def set_unit_stats(self):
        stats = {
            'Sword': {'hp': 100, 'atk': 15, 'speed': 0.02, 'range': 0.08, 'color': RED if self.team == 'red' else BLUE},
            'Archer': {'hp': 80, 'atk': 20, 'speed': 0.015, 'range': 0.3, 'color': GREEN},
            'Shield': {'hp': 150, 'atk': 10, 'speed': 0.01, 'range': 0.07, 'defense': 0.5, 'color': GRAY},
            'Spear': {'hp': 90, 'atk': 25, 'speed': 0.025, 'range': 0.12, 'color': YELLOW},
            'Tank': {'hp': 300, 'atk': 50, 'speed': 0.008, 'range': 0.4, 'color': DARK_GRAY}
        }
        s = stats[self.unit_type]
        self.max_hp = self.hp = s['hp']
        self.attack = s['atk']
        self.speed = s['speed']
        self.range = s['range']
        self.color = s['color']
        self.defense = s.get('defense', 0)
        
    def find_target(self, enemies):
        if not self.alive:
            return
        closest = None
        closest_dist = float('inf')
        for enemy in enemies:
            if enemy.alive:
                dist = abs(enemy.x - self.x)
                if dist < closest_dist:
                    closest_dist = dist
                    closest = enemy
        self.target = closest
        
    def update(self, enemies, projectiles, frame):
        if not self.alive:
            return
            
        self.find_target(enemies)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        self.anim_frame = frame
        
        if self.target and self.target.alive:
            dist = abs(self.target.x - self.x)
            
            if dist <= self.range:
                if self.attack_cooldown <= 0:
                    self.attack_target(projectiles)
                    self.attack_cooldown = 30
                    self.state = 'attack'
            else:
                self.state = 'move'
                if self.target.x > self.x:
                    self.x += self.speed
                    self.direction = 1
                else:
                    self.x -= self.speed
                    self.direction = -1
        else:
            self.state = 'idle'
            
        # 更新特效
        for effect in self.effects[:]:
            effect['frame'] += 1
            if effect['frame'] > effect['duration']:
                self.effects.remove(effect)
                
    def attack_target(self, projectiles):
        if self.unit_type == 'Sword':
            self.effects.append({'type': 'slash', 'frame': 0, 'duration': 10})
            if random.random() < 0.7:
                damage = self.attack + random.randint(-3, 3)
                self.target.take_damage(damage)
                self.target.effects.append({
                    'type': 'damage', 'value': damage, 'frame': 0, 'duration': 20,
                    'x': self.target.x, 'y': self.target.y + 0.15
                })
                
        elif self.unit_type == 'Archer':
            projectiles.append(Arrow(self.x, self.y + 0.1, self.target, self.attack))
            
        elif self.unit_type == 'Shield':
            self.effects.append({'type': 'shield_bash', 'frame': 0, 'duration': 15})
            damage = self.attack + random.randint(-2, 2)
            self.target.take_damage(damage)
            self.target.effects.append({
                'type': 'damage', 'value': damage, 'frame': 0, 'duration': 20,
                'x': self.target.x, 'y': self.target.y + 0.15
            })
            
        elif self.unit_type == 'Spear':
            self.effects.append({'type': 'lunge', 'frame': 0, 'duration': 12})
            self.x += 0.03 * self.direction
            damage = self.attack + random.randint(-5, 5)
            self.target.take_damage(damage)
            self.target.effects.append({
                'type': 'damage', 'value': damage, 'frame': 0, 'duration': 20,
                'x': self.target.x, 'y': self.target.y + 0.15
            })
            
        elif self.unit_type == 'Tank':
            projectiles.append(Shell(self.x, self.y + 0.08, self.target, self.attack))
            
    def take_damage(self, damage):
        damage = int(damage * (1 - self.defense))
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.state = 'dead'

class Arrow:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 0.04
        self.alive = True
        
    def update(self):
        if not self.alive or not self.target.alive:
            self.alive = False
            return
            
        dx = self.target.x - self.x
        dy = (self.target.y + 0.1) - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 0.02:
            damage = self.damage + random.randint(-3, 3)
            self.target.take_damage(damage)
            self.target.effects.append({
                'type': 'damage', 'value': damage, 'frame': 0, 'duration': 20,
                'x': self.target.x, 'y': self.target.y + 0.15
            })
            self.alive = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
            
class Shell:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 0.03
        self.alive = True
        self.trail = []
        
    def update(self):
        if not self.alive:
            return
            
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
            
        dx = self.target.x - self.x
        dy = (self.target.y + 0.08) - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 0.03:
            damage = self.damage + random.randint(-10, 10)
            self.target.take_damage(damage)
            self.target.effects.append({
                'type': 'damage', 'value': damage, 'frame': 0, 'duration': 20,
                'x': self.target.x, 'y': self.target.y + 0.2
            })
            self.alive = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

def draw_stickman(ax, unit):
    if not unit.alive:
        # 死亡状态
        x, y = unit.x, unit.y
        ax.plot([x, x + 0.04 * unit.direction], [y - 0.02, y], 'k-', linewidth=1.5)
        ax.plot([x + 0.04 * unit.direction, x + 0.07 * unit.direction], [y, y - 0.01], 'k-', linewidth=1.5)
        ax.add_patch(plt.Circle((x, y + 0.02), 0.015, fill=False, color='gray', linewidth=1.5))
        return
        
    x, y = unit.x, unit.y
    walk = math.sin(unit.anim_frame * 0.3) * 0.005 if unit.state == 'move' else 0
    
    # 头
    ax.add_patch(plt.Circle((x, y + 0.12), 0.015, fill=False, color=unit.color, linewidth=2))
    
    # 身体
    ax.plot([x, x], [y + 0.105, y + 0.06], color=unit.color, linewidth=2)
    
    # 手臂
    if unit.state == 'attack':
        if unit.unit_type == 'Sword':
            # 挥刀动作 - 大幅度弧线
            angle = math.sin(unit.anim_frame * 0.5) * 1.2
            hand_x = x + 0.08 * unit.direction * math.cos(angle)
            hand_y = y + 0.08 + 0.06 * math.sin(angle)
            ax.plot([x, hand_x], [y + 0.08, hand_y], color=unit.color, linewidth=3)
        elif unit.unit_type == 'Spear':
            # 刺击动作
            thrust = math.sin(unit.anim_frame * 0.8) * 0.05
            hand_x = x + (0.04 + thrust) * unit.direction
            hand_y = y + 0.08
            ax.plot([x, hand_x], [y + 0.08, hand_y], color=unit.color, linewidth=3)
        else:
            ax.plot([x, x + 0.03 * unit.direction], [y + 0.08, y + 0.09], color=unit.color, linewidth=2)
            ax.plot([x, x - 0.01 * unit.direction], [y + 0.08, y + 0.06], color=unit.color, linewidth=2)
    else:
        ax.plot([x, x + 0.025 * unit.direction], [y + 0.08, y + 0.085 + walk], color=unit.color, linewidth=2)
        ax.plot([x, x - 0.01 * unit.direction], [y + 0.08, y + 0.065 - walk], color=unit.color, linewidth=2)
    
    # 腿
    leg = math.sin(unit.anim_frame * 0.3) * 0.015 if unit.state == 'move' else 0
    ax.plot([x, x + leg], [y + 0.06, y + 0.025], color=unit.color, linewidth=2)
    ax.plot([x, x - leg], [y + 0.06, y + 0.025], color=unit.color, linewidth=2)
    ax.plot([x + leg, x + leg * 1.2], [y + 0.025, y], color=unit.color, linewidth=2)
    ax.plot([x - leg, x - leg * 1.2], [y + 0.025, y], color=unit.color, linewidth=2)
    
    # 武器
    draw_weapon(ax, unit)
    
    # 特效
    draw_effects(ax, unit)
    
    # 血条
    hp_pct = unit.hp / unit.max_hp
    hp_color = '#00AA00' if hp_pct > 0.6 else '#FFAA00' if hp_pct > 0.3 else '#FF0000'
    ax.add_patch(patches.Rectangle((x - 0.03, y + 0.16), 0.06 * hp_pct, 0.008, facecolor=hp_color))
    ax.add_patch(patches.Rectangle((x - 0.03, y + 0.16), 0.06, 0.008, fill=False, edgecolor='black', linewidth=0.5))
    
    # 兵种标签
    ax.text(x, y + 0.2, unit.unit_type, ha='center', va='bottom', fontsize=7, color=unit.color)

def draw_weapon(ax, unit):
    x, y = unit.x, unit.y
    
    if unit.unit_type == 'Sword':
        hand_x = x + 0.04 * unit.direction
        hand_y = y + 0.08
        blade_x = hand_x + 0.05 * unit.direction
        blade_y = hand_y + 0.02
        ax.plot([hand_x, blade_x], [hand_y, blade_y], color=GRAY, linewidth=3)
        ax.plot([hand_x + 0.005 * unit.direction, blade_x + 0.005 * unit.direction],
                [hand_y, blade_y], color='white', linewidth=1.5)

    elif unit.unit_type == 'Archer':
        bow_x = x - 0.015 * unit.direction
        theta = np.linspace(0.5, 2.5, 20)
        bx = bow_x + 0.02 * np.cos(theta)
        by = y + 0.09 + 0.03 * np.sin(theta)
        ax.plot(bx, by, color='#8B4513', linewidth=2)

    elif unit.unit_type == 'Shield':
        shield_x = x + 0.035 * unit.direction
        shield = patches.Ellipse((shield_x, y + 0.085), 0.025, 0.04, color='#8B4513')
        ax.add_patch(shield)

    elif unit.unit_type == 'Spear':
        spear_x = x + 0.025 * unit.direction
        ax.plot([spear_x, spear_x + 0.08 * unit.direction], [y + 0.03, y + 0.12],
                color='#8B4513', linewidth=3)
        tip_x = spear_x + 0.08 * unit.direction
        ax.add_patch(patches.Polygon([(tip_x, y + 0.12),
                                      (tip_x + 0.01 * unit.direction, y + 0.14),
                                      (tip_x - 0.005 * unit.direction, y + 0.14)],
                                     color=GRAY))

    elif unit.unit_type == 'Tank':
        barrel_x = x + 0.06 * unit.direction
        ax.plot([barrel_x, barrel_x + 0.08 * unit.direction], [y + 0.09, y + 0.09],
                color=DARK_GRAY, linewidth=4)
        ax.plot([barrel_x + 0.07 * unit.direction, barrel_x + 0.09 * unit.direction],
                [y + 0.085, y + 0.095], color=BLACK, linewidth=3)

def draw_effects(ax, unit):
    for effect in unit.effects:
        if effect['type'] == 'slash':
            # 刀光特效 - 更大更明显
            progress = effect['frame'] / effect['duration']
            alpha = 1 - progress
            x = unit.x + 0.06 * unit.direction
            y = unit.y + 0.09
            # 挥刀弧线
            swing_angle = progress * 1.5
            for i in range(5):
                angle_offset = (i - 2) * 0.1 + swing_angle * unit.direction
                px = x + 0.08 * unit.direction * math.cos(angle_offset)
                py = y + 0.05 * math.sin(angle_offset)
                ax.add_patch(plt.Circle((px, py), 0.015 * (1-progress),
                                       facecolor=(1, 1, 0.5, alpha * 0.8), edgecolor='yellow', linewidth=1))
            
        elif effect['type'] == 'shield_bash':
            # 盾击特效 - 冲击波
            x = unit.x + 0.05 * unit.direction
            y = unit.y + 0.08
            progress = effect['frame'] / effect['duration']
            for i in range(3):
                size = 0.02 + (progress + i * 0.1) * 0.03
                alpha = 0.6 - progress * 0.5 - i * 0.15
                if alpha > 0:
                    circle = plt.Circle((x, y), size, fill=False, 
                                       color=(0.9, 0.9, 0.5, alpha), linewidth=3)
                    ax.add_patch(circle)
            
        elif effect['type'] == 'lunge':
            # 冲刺残影 - 更明显
            for i in range(5):
                offset = (i + 1) * 0.04 * unit.direction
                ghost_x = unit.x - offset
                alpha = 0.5 - i * 0.1
                # 画完整的火柴人残影
                ax.add_patch(plt.Circle((ghost_x, unit.y + 0.12), 0.015, fill=False, 
                                       color=(1, 1, 0, alpha), linewidth=2))
                ax.plot([ghost_x, ghost_x], [unit.y + 0.105, unit.y + 0.06], 
                       color=(1, 1, 0, alpha), linewidth=2)
                ax.plot([ghost_x, ghost_x + 0.025 * unit.direction], 
                       [unit.y + 0.08, unit.y + 0.085], color=(1, 1, 0, alpha), linewidth=2)
                
        elif effect['type'] == 'damage':
            x, y = effect['x'], effect['y'] + effect['frame'] * 0.003
            alpha = 1 - (effect['frame'] / effect['duration'])
            ax.text(x, y, f"-{effect['value']}", ha='center', va='center',
                   fontsize=10, color=(1, 0, 0, alpha), fontweight='bold')

def draw_projectiles(ax, projectiles):
    for proj in projectiles:
        if not proj.alive:
            continue
        if isinstance(proj, Arrow):
            angle = math.atan2(proj.target.y + 0.1 - proj.y, proj.target.x - proj.x)
            end_x = proj.x - math.cos(angle) * 0.03
            end_y = proj.y - math.sin(angle) * 0.03
            ax.plot([end_x, proj.x], [end_y, proj.y], color='#8B4513', linewidth=2)
            ax.add_patch(patches.Polygon([(proj.x, proj.y),
                                          (proj.x - 0.005 * math.cos(angle - 0.5), proj.y - 0.005 * math.sin(angle - 0.5)),
                                          (proj.x - 0.005 * math.cos(angle + 0.5), proj.y - 0.005 * math.sin(angle + 0.5))],
                                         color=GRAY))
        elif isinstance(proj, Shell):
            for i, pos in enumerate(proj.trail):
                alpha = i / len(proj.trail) if proj.trail else 0
                size = 2 + i // 2
                color = (1, 0.4 + i * 0.1, 0)
                ax.add_patch(plt.Circle((pos[0], pos[1]), size * 0.001, facecolor=color, alpha=alpha))
            ax.add_patch(plt.Circle((proj.x, proj.y), 0.008, facecolor=BLACK))
            ax.add_patch(plt.Circle((proj.x, proj.y), 0.005, facecolor=RED))

# 初始化战斗
unit_types = ['Sword', 'Archer', 'Shield', 'Spear', 'Tank']
red_team = [StickMan(0.15 + i * 0.08, GROUND_Y, 'red', unit_types[i]) for i in range(5)]
blue_team = [StickMan(0.85 - i * 0.08, GROUND_Y, 'blue', unit_types[i]) for i in range(5)]
projectiles = []

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('#87CEEB')

# 地面
ax.axhline(y=GROUND_Y, color='#228B22', linewidth=3)
ax.fill_between([0, 1], 0, GROUND_Y, color='#228B22', alpha=0.5)

def animate(frame):
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#87CEEB')
    ax.axhline(y=GROUND_Y, color='#228B22', linewidth=3)
    ax.fill_between([0, 1], 0, GROUND_Y, color='#228B22', alpha=0.5)
    
    # 更新
    for unit in red_team:
        unit.update(blue_team, projectiles, frame)
    for unit in blue_team:
        unit.update(red_team, projectiles, frame)
    for proj in projectiles[:]:
        proj.update()
        if not proj.alive:
            projectiles.remove(proj)
    
    # 绘制
    draw_projectiles(ax, projectiles)
    for unit in red_team:
        draw_stickman(ax, unit)
    for unit in blue_team:
        draw_stickman(ax, unit)
    
    # UI
    red_alive = sum(1 for u in red_team if u.alive)
    blue_alive = sum(1 for u in blue_team if u.alive)
    ax.text(0.05, 0.45, f'Red: {red_alive}/5', fontsize=12, color=RED, fontweight='bold')
    ax.text(0.85, 0.45, f'Blue: {blue_alive}/5', fontsize=12, color=BLUE, fontweight='bold')
    
    if red_alive == 0:
        ax.text(0.5, 0.35, 'Blue Wins!', fontsize=24, ha='center', color=BLUE, fontweight='bold')
    elif blue_alive == 0:
        ax.text(0.5, 0.35, 'Red Wins!', fontsize=24, ha='center', color=RED, fontweight='bold')

print("Generating battle animation...")
anim = FuncAnimation(fig, animate, frames=200, interval=50, blit=False)
writer = PillowWriter(fps=20)
anim.save('/root/.openclaw/workspace/battle.gif', writer=writer)
plt.close()
print("Saved to battle.gif")

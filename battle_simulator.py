import pygame
import random
import math

# 初始化
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("火柴人军团战斗模拟器")
clock = pygame.time.Clock()

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GROUND_Y = 600

class StickMan:
    def __init__(self, x, y, team, unit_type):
        self.x = x
        self.y = y
        self.team = team  # 'red' or 'blue'
        self.unit_type = unit_type
        self.alive = True
        self.direction = 1 if team == 'red' else -1
        
        # 根据兵种设置属性
        self.set_unit_stats()
        
        # 动画相关
        self.anim_frame = 0
        self.anim_timer = 0
        self.state = 'idle'  # idle, move, attack, dead
        self.attack_cooldown = 0
        self.target = None
        
        # 特效
        self.effects = []  # 存储特效
        
    def set_unit_stats(self):
        if self.unit_type == '步兵':
            self.hp = self.max_hp = 100
            self.attack = 15
            self.speed = 2
            self.range = 40
            self.attack_speed = 30
            self.color = RED if self.team == 'red' else BLUE
        elif self.unit_type == '工兵':
            self.hp = self.max_hp = 80
            self.attack = 20
            self.speed = 1.5
            self.range = 200
            self.attack_speed = 60
            self.color = GREEN
        elif self.unit_type == '盾兵':
            self.hp = self.max_hp = 150
            self.attack = 10
            self.speed = 1
            self.range = 35
            self.attack_speed = 40
            self.defense = 0.5
            self.color = GRAY
        elif self.unit_type == '矛兵':
            self.hp = self.max_hp = 90
            self.attack = 25
            self.speed = 2.5
            self.range = 60
            self.attack_speed = 45
            self.color = YELLOW
        elif self.unit_type == '坦克':
            self.hp = self.max_hp = 300
            self.attack = 50
            self.speed = 0.8
            self.range = 300
            self.attack_speed = 90
            self.color = DARK_GRAY
            
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
        
    def update(self, enemies, projectiles):
        if not self.alive:
            return
            
        self.find_target(enemies)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 动画更新
        self.anim_timer += 1
        if self.anim_timer > 5:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
            
        if self.target and self.target.alive:
            dist = abs(self.target.x - self.x)
            
            if dist <= self.range:
                # 在攻击范围内，攻击
                if self.attack_cooldown <= 0:
                    self.attack_target(projectiles)
                    self.attack_cooldown = self.attack_speed
                    self.state = 'attack'
            else:
                # 移动向目标
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
        if self.unit_type == '步兵':
            # 步兵：挥刀斩击
            self.effects.append({
                'type': 'slash',
                'frame': 0,
                'duration': 10
            })
            if random.random() < 0.7:  # 70%命中率
                damage = self.attack + random.randint(-3, 3)
                self.target.take_damage(damage)
                # 显示伤害数字
                self.target.effects.append({
                    'type': 'damage',
                    'value': damage,
                    'frame': 0,
                    'duration': 30,
                    'x': self.target.x,
                    'y': self.target.y - 50
                })
                
        elif self.unit_type == '工兵':
            # 工兵：射箭
            projectiles.append(Arrow(self.x, self.y - 40, self.target, self.attack, self.team))
            
        elif self.unit_type == '盾兵':
            # 盾兵：用盾前冲抵挡
            self.effects.append({
                'type': 'shield_bash',
                'frame': 0,
                'duration': 15
            })
            # 盾兵有概率完全格挡
            if random.random() < 0.3:
                self.effects.append({
                    'type': 'block',
                    'frame': 0,
                    'duration': 20
                })
            else:
                damage = self.attack + random.randint(-2, 2)
                self.target.take_damage(damage)
                self.target.effects.append({
                    'type': 'damage',
                    'value': damage,
                    'frame': 0,
                    'duration': 30,
                    'x': self.target.x,
                    'y': self.target.y - 50
                })
                
        elif self.unit_type == '矛兵':
            # 矛兵：长矛冲刺
            self.effects.append({
                'type': 'lunge',
                'frame': 0,
                'duration': 12
            })
            # 冲刺位移
            dash_distance = 30 * self.direction
            self.x += dash_distance
            damage = self.attack + random.randint(-5, 5)
            self.target.take_damage(damage)
            self.target.effects.append({
                'type': 'damage',
                'value': damage,
                'frame': 0,
                'duration': 30,
                'x': self.target.x,
                'y': self.target.y - 50
            })
            
        elif self.unit_type == '坦克':
            # 坦克：开炮
            projectiles.append(Shell(self.x, self.y - 30, self.target, self.attack, self.team))
            
    def take_damage(self, damage):
        if hasattr(self, 'defense'):
            damage = int(damage * (1 - self.defense))
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.state = 'dead'
            
    def draw(self, screen):
        if not self.alive:
            # 绘制死亡状态（躺在地上）
            self.draw_dead(screen)
            return
            
        # 绘制火柴人
        self.draw_stickman(screen)
        
        # 绘制武器
        self.draw_weapon(screen)
        
        # 绘制特效
        self.draw_effects(screen)
        
        # 绘制血条
        self.draw_health_bar(screen)
        
    def draw_stickman(self, screen):
        x, y = int(self.x), int(self.y)
        walk_offset = math.sin(self.anim_frame * 0.5) * 3 if self.state == 'move' else 0
        
        # 头
        pygame.draw.circle(screen, self.color, (x, y - 70), 8, 2)
        
        # 身体
        pygame.draw.line(screen, self.color, (x, y - 62), (x, y - 35), 2)
        
        # 手臂 - 根据状态变化
        if self.state == 'attack':
            # 攻击姿势
            if self.unit_type == '步兵':
                # 挥刀动作
                attack_angle = math.sin(self.anim_frame * 0.8) * 1.5
                hand_x = x + int(25 * self.direction * math.cos(attack_angle))
                hand_y = y - 50 + int(20 * math.sin(attack_angle))
                pygame.draw.line(screen, self.color, (x, y - 50), (hand_x, hand_y), 2)
            elif self.unit_type == '盾兵':
                # 举盾姿势
                pygame.draw.line(screen, self.color, (x, y - 50), (x + 15 * self.direction, y - 45), 3)
                pygame.draw.line(screen, self.color, (x, y - 50), (x - 5 * self.direction, y - 35), 2)
            else:
                pygame.draw.line(screen, self.color, (x, y - 50), (x + 15 * self.direction, y - 45), 2)
                pygame.draw.line(screen, self.color, (x, y - 50), (x - 5 * self.direction, y - 35), 2)
        else:
            # 正常/移动姿势
            pygame.draw.line(screen, self.color, (x, y - 50), (x + 12 * self.direction, y - 45 + walk_offset), 2)
            pygame.draw.line(screen, self.color, (x, y - 50), (x - 5 * self.direction, y - 35 - walk_offset), 2)
        
        # 腿
        leg_swing = math.sin(self.anim_frame * 0.5) * 8 if self.state == 'move' else 0
        pygame.draw.line(screen, self.color, (x, y - 35), (x + leg_swing, y - 15), 2)
        pygame.draw.line(screen, self.color, (x, y - 35), (x - leg_swing, y - 15), 2)
        pygame.draw.line(screen, self.color, (x + leg_swing, y - 15), (x + leg_swing * 1.5, y), 2)
        pygame.draw.line(screen, self.color, (x - leg_swing, y - 15), (x - leg_swing * 1.5, y), 2)
        
    def draw_weapon(self, screen):
        x, y = int(self.x), int(self.y)
        
        if self.unit_type == '步兵':
            # 绘制刀
            hand_x = x + 20 * self.direction
            hand_y = y - 50
            blade_end_x = hand_x + 25 * self.direction
            blade_end_y = hand_y - 10
            pygame.draw.line(screen, GRAY, (hand_x, hand_y), (blade_end_x, blade_end_y), 3)
            pygame.draw.line(screen, WHITE, (hand_x + 3*self.direction, hand_y), (blade_end_x + 3*self.direction, blade_end_y), 2)
            
        elif self.unit_type == '工兵':
            # 绘制弓（背在身上）
            bow_x = x - 8 * self.direction
            pygame.draw.arc(screen, (139, 69, 19), (bow_x - 10, y - 60, 20, 30), 0.5, 2.5, 2)
            
        elif self.unit_type == '盾兵':
            # 绘制盾牌
            shield_x = x + 18 * self.direction
            pygame.draw.ellipse(screen, (139, 69, 19), (shield_x - 12, y - 55, 24, 35))
            pygame.draw.ellipse(screen, (160, 82, 45), (shield_x - 8, y - 50, 16, 25))
            
        elif self.unit_type == '矛兵':
            # 绘制长矛
            spear_x = x + 15 * self.direction
            pygame.draw.line(screen, (139, 69, 19), (spear_x, y - 20), (spear_x + 40 * self.direction, y - 70), 3)
            pygame.draw.polygon(screen, GRAY, [
                (spear_x + 40 * self.direction, y - 70),
                (spear_x + 45 * self.direction, y - 80),
                (spear_x + 35 * self.direction, y - 80)
            ])
            
        elif self.unit_type == '坦克':
            # 绘制坦克炮管
            barrel_x = x + 30 * self.direction
            pygame.draw.rect(screen, DARK_GRAY, (barrel_x, y - 45, 40, 8))
            pygame.draw.rect(screen, BLACK, (barrel_x + 35, y - 47, 10, 12))
            
    def draw_effects(self, screen):
        for effect in self.effects:
            if effect['type'] == 'slash':
                # 刀光特效
                alpha = 255 - (effect['frame'] * 25)
                x = int(self.x + 30 * self.direction)
                y = int(self.y - 55)
                points = [
                    (x, y - 20),
                    (x + 30 * self.direction, y),
                    (x + 20 * self.direction, y + 15),
                    (x - 10 * self.direction, y + 5)
                ]
                pygame.draw.polygon(screen, (255, 255, 200), points)
                
            elif effect['type'] == 'shield_bash':
                # 盾击特效
                x = int(self.x + 25 * self.direction)
                y = int(self.y - 40)
                size = 20 + effect['frame'] * 2
                pygame.draw.circle(screen, (200, 200, 200), (x, y), size, 2)
                
            elif effect['type'] == 'block':
                # 格挡特效
                x = int(self.x + 20 * self.direction)
                y = int(self.y - 50)
                pygame.draw.polygon(screen, (255, 215, 0), [
                    (x, y - 25),
                    (x + 10, y - 15),
                    (x, y - 5),
                    (x - 10, y - 15)
                ])
                
            elif effect['type'] == 'lunge':
                # 冲刺特效（残影）
                for i in range(3):
                    offset = (i + 1) * 15 * self.direction
                    alpha = 150 - i * 40
                    ghost_x = int(self.x - offset)
                    pygame.draw.circle(screen, (255, 255, 0), (ghost_x, int(self.y) - 50), 5)
                    
            elif effect['type'] == 'damage':
                # 伤害数字
                x = effect['x']
                y = effect['y'] - effect['frame'] * 2
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"-{effect['value']}", True, RED)
                screen.blit(text, (x - 10, y))
                
    def draw_health_bar(self, screen):
        bar_width = 40
        bar_height = 5
        x = int(self.x - bar_width // 2)
        y = int(self.y - 90)
        
        # 背景
        pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height))
        # 血量
        hp_percent = self.hp / self.max_hp
        hp_color = GREEN if hp_percent > 0.6 else YELLOW if hp_percent > 0.3 else RED
        pygame.draw.rect(screen, hp_color, (x, y, int(bar_width * hp_percent), bar_height))
        
    def draw_dead(self, screen):
        # 绘制倒下的火柴人
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, GRAY, (x, y - 10), 8, 2)
        pygame.draw.line(screen, GRAY, (x, y - 2), (x + 20 * self.direction, y), 2)
        pygame.draw.line(screen, GRAY, (x + 20 * self.direction, y), (x + 35 * self.direction, y - 5), 2)
        pygame.draw.line(screen, GRAY, (x, y - 2), (x - 10, y + 5), 2)

class Arrow:
    def __init__(self, x, y, target, damage, team):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.team = team
        self.speed = 8
        self.alive = True
        
    def update(self):
        if not self.alive or not self.target.alive:
            self.alive = False
            return
            
        dx = self.target.x - self.x
        dy = (self.target.y - 40) - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 10:
            # 命中
            actual_damage = self.damage + random.randint(-3, 3)
            self.target.take_damage(actual_damage)
            self.target.effects.append({
                'type': 'damage',
                'value': actual_damage,
                'frame': 0,
                'duration': 30,
                'x': self.target.x,
                'y': self.target.y - 50
            })
            self.alive = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
            
    def draw(self, screen):
        if not self.alive:
            return
        angle = math.atan2(self.target.y - 40 - self.y, self.target.x - self.x)
        end_x = self.x - math.cos(angle) * 15
        end_y = self.y - math.sin(angle) * 15
        pygame.draw.line(screen, (139, 69, 19), (end_x, end_y), (self.x, self.y), 2)
        pygame.draw.polygon(screen, GRAY, [
            (self.x, self.y),
            (self.x - 5 * math.cos(angle - 0.5), self.y - 5 * math.sin(angle - 0.5)),
            (self.x - 5 * math.cos(angle + 0.5), self.y - 5 * math.sin(angle + 0.5))
        ])

class Shell:
    def __init__(self, x, y, target, damage, team):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.team = team
        self.speed = 6
        self.alive = True
        self.trail = []
        
    def update(self):
        if not self.alive:
            return
            
        # 记录轨迹
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
            
        dx = self.target.x - self.x
        dy = (self.target.y - 30) - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 15:
            # 爆炸
            actual_damage = self.damage + random.randint(-10, 10)
            self.target.take_damage(actual_damage)
            self.target.effects.append({
                'type': 'damage',
                'value': actual_damage,
                'frame': 0,
                'duration': 30,
                'x': self.target.x,
                'y': self.target.y - 60
            })
            # 范围伤害
            self.explode()
            self.alive = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
            
    def explode(self):
        # 对周围敌人造成伤害
        pass  # 简化版，只打目标
        
    def draw(self, screen):
        if not self.alive:
            return
        # 绘制轨迹
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            size = 2 + i // 3
            pygame.draw.circle(screen, (255, 100 + i * 15, 0), (int(pos[0]), int(pos[1])), size)
        # 绘制炮弹
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 3)

class BattleSimulator:
    def __init__(self):
        self.red_team = []
        self.blue_team = []
        self.projectiles = []
        self.winner = None
        self.battle_log = []
        
    def setup_battle(self):
        # 红方军团
        unit_types = ['步兵', '工兵', '盾兵', '矛兵', '坦克']
        for i, unit_type in enumerate(unit_types):
            x = 100 + i * 80
            self.red_team.append(StickMan(x, GROUND_Y, 'red', unit_type))
            
        # 蓝方军团
        for i, unit_type in enumerate(unit_types):
            x = WIDTH - 100 - i * 80
            self.blue_team.append(StickMan(x, GROUND_Y, 'blue', unit_type))
            
    def update(self):
        if self.winner:
            return
            
        # 更新红方
        for unit in self.red_team:
            unit.update(self.blue_team, self.projectiles)
            
        # 更新蓝方
        for unit in self.blue_team:
            unit.update(self.red_team, self.projectiles)
            
        # 更新投射物
        for proj in self.projectiles[:]:
            proj.update()
            if not proj.alive:
                self.projectiles.remove(proj)
                
        # 检查胜负
        red_alive = sum(1 for u in self.red_team if u.alive)
        blue_alive = sum(1 for u in self.blue_team if u.alive)
        
        if red_alive == 0:
            self.winner = '蓝方'
        elif blue_alive == 0:
            self.winner = '红方'
            
    def draw(self, screen):
        # 背景
        screen.fill((135, 206, 235))  # 天空蓝
        
        # 地面
        pygame.draw.rect(screen, (34, 139, 34), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        
        # 绘制投射物
        for proj in self.projectiles:
            proj.draw(screen)
            
        # 绘制红方
        for unit in self.red_team:
            unit.draw(screen)
            
        # 绘制蓝方
        for unit in self.blue_team:
            unit.draw(screen)
            
        # 绘制UI
        self.draw_ui(screen)
        
        # 绘制胜负
        if self.winner:
            font = pygame.font.SysFont(None, 72)
            text = font.render(f"{self.winner}获胜!", True, YELLOW)
            screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
            
    def draw_ui(self, screen):
        font = pygame.font.SysFont(None, 24)
        
        # 红方信息
        red_alive = sum(1 for u in self.red_team if u.alive)
        text = font.render(f"红方: {red_alive}/{len(self.red_team)}", True, RED)
        screen.blit(text, (20, 20))
        
        # 蓝方信息
        blue_alive = sum(1 for u in self.blue_team if u.alive)
        text = font.render(f"蓝方: {blue_alive}/{len(self.blue_team)}", True, BLUE)
        screen.blit(text, (WIDTH - 150, 20))
        
        # 兵种说明
        y_offset = 50
        for i, unit_type in enumerate(['步兵', '工兵', '盾兵', '矛兵', '坦克']):
            text = font.render(f"{unit_type}", True, BLACK)
            screen.blit(text, (20, y_offset + i * 25))
            
# 主循环
def main():
    simulator = BattleSimulator()
    simulator.setup_battle()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # R键重新开始
                    simulator = BattleSimulator()
                    simulator.setup_battle()
                elif event.key == pygame.K_SPACE:  # 空格暂停
                    pass
                    
        simulator.update()
        simulator.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()

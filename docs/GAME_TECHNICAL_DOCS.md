# ⚔️ 征服者 - 技术文档

**版本**: v1.0  
**最后更新**: 2026-04-10  
**主分支**: master  
**文件路径**: `game_public/index.html`

---

## 📋 目录

1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [核心系统](#核心系统)
4. [数据结构](#数据结构)
5. [功能模块详解](#功能模块详解)
6. [UI/UX 设计](#uiux-设计)
7. [性能优化](#性能优化)
8. [扩展指南](#扩展指南)

---

## 项目概述

### 游戏简介
《征服者》是一款基于 HTML5 + CSS3 + JavaScript 的轻量级策略战争游戏，采用纯前端技术实现，无需任何后端服务。

### 核心特性
- 🗺️ **地图征战**: 8 个不同难度的领地
- ⚔️ **兵种系统**: 6 种特色兵种，各具特点
- 📈 **难度成长**: 动态难度系统，随胜利次数提升
- 💰 **经济系统**: 金币招募、升级、解锁
- 🎨 **深色主题**: 现代化 UI 设计

### 技术栈
- **HTML5**: 语义化结构
- **CSS3**: 渐变、动画、响应式布局
- **JavaScript (ES6+)**: 游戏逻辑、状态管理
- **零依赖**: 无需第三方库

---

## 技术架构

### 文件结构
```
gamefrommyboy/
├── game_public/
│   └── index.html          # 主游戏文件 (~1500 行)
├── docs/
│   └── GAME_TECHNICAL_DOCS.md  # 技术文档
└── README.md               # 项目说明
```

### 代码组织
```javascript
// 1. 游戏数据 (gameData 对象)
const gameData = {
  gold, victoryCount, difficultyScale,
  currentTarget, recruitedUnits,
  targets: [], units: [], unitLevels: {}
}

// 2. 初始化系统
initGame() → initUnitLevels() → renderMap() → updateUI()

// 3. 核心系统
- 地图系统：renderMap(), selectTarget()
- 兵种系统：getUnitStats(), recruitUnit()
- 战斗系统：startBattle(), showResult()
- 解锁系统：showUnlockModal(), unlockUnit()

// 4. UI 更新
updateUI(), updatePlayerStats(), renderUnitsCarousel()
```

### 状态管理
```javascript
// 单一数据源 (Single Source of Truth)
gameData → 所有 UI 从此渲染

// 状态更新流程
用户操作 → 修改 gameData → 调用 updateUI() → 重新渲染
```

---

## 核心系统

### 1. 难度成长系统

#### 难度计算公式
```javascript
难度倍率 = 1 + (胜利次数 × 0.12) + (胜利次数² × 0.005)
```

#### 难度成长表
| 胜利次数 | 难度倍率 | 敌人强度 |
|---------|---------|---------|
| 0 场 | 100% | 基础 |
| 5 场 | 172% | +72% |
| 10 场 | 270% | +170% |
| 20 场 | 540% | +440% |

#### 实现代码
```javascript
// 应用难度到敌人属性
const scaledAttack = Math.floor(
  gameData.currentTarget.attack * gameData.difficultyScale
);
const scaledDefense = Math.floor(
  gameData.currentTarget.defense * gameData.difficultyScale
);

// 胜利后更新难度
gameData.victoryCount++;
gameData.difficultyScale = 1 + (
  gameData.victoryCount * 0.12
) + (
  gameData.victoryCount * gameData.victoryCount * 0.005
);
```

---

### 2. 兵种系统

#### 兵种数据
```javascript
units: [
  {
    id: 'infantry',
    name: '步兵',
    emoji: '⚔️',
    unlocked: true,
    unlockCost: 0,
    baseCost: 50,
    baseAttack: 20,
    baseHp: 100
  },
  // ... 其他 5 个兵种
]
```

#### 属性成长
```javascript
// 升级 multiplier
multiplier = 1 + (level - 1) * 0.2;  // 每级 +20%

// 升级成本成长
upgradeCost = Math.floor(previousCost * 1.5);  // 每级 ×1.5
```

#### 兵种克制关系 (设计文档)
```
        ⚔️ 步兵
       /      \
   克制      被克
     ↓          ↓
  🐴骑兵 ←→ 🏹弓箭手

克制加成:
- 克制方：攻击 +40%, 防御 +20%, 暴击 +10%
- 被克方：攻击 -25%, 防御 -30%, 暴击 -5%
- 长矛兵 vs 骑兵：攻击 +60%, 防御 +30%
```

---

### 3. 战斗系统

#### 战斗流程
```javascript
function startBattle() {
  // 1. 计算双方属性
  const totalAttack = recruitedUnits.reduce(...)
  const totalDefense = recruitedUnits.reduce(...)
  const enemyAttack = baseAttack * difficultyScale
  
  // 2. 回合制模拟
  while (playerHp > 0 && enemyHp > 0) {
    enemyHp -= totalAttack;
    if (enemyHp <= 0) break;
    playerHp -= enemyAttack;
  }
  
  // 3. 判定胜负
  const isVictory = playerHp > 0;
  
  // 4. 结算奖励
  if (isVictory) {
    gold += reward;
    victoryCount++;
    updateDifficulty();
  }
  
  // 5. 显示结果
  showResult(isVictory, damageDealt, goldEarned);
}
```

#### 战斗统计
- 造成伤害
- 获得金币
- 战斗回合数
- 难度倍率

---

### 4. 经济系统

#### 金币获取
```javascript
// 基础奖励
reward = target.reward;

// 胜利后
gold += reward;
```

#### 金币消耗
```javascript
// 招募兵种
gold -= unit.baseCost * levelMultiplier;

// 升级兵种
gold -= levelData.upgradeCost;
levelData.upgradeCost *= 1.5;

// 解锁兵种
gold -= unit.unlockCost;
```

---

## 数据结构

### gameData 对象
```javascript
const gameData = {
  // 资源
  gold: Number,              // 当前金币
  victoryCount: Number,      // 胜利场次
  difficultyScale: Number,   // 难度倍率
  
  // 状态
  currentTarget: Object,     // 当前选择的敌人
  recruitedUnits: Array,     // 已招募的兵种
  
  // 配置
  targets: Array,            // 所有地图目标
  units: Array,              // 所有兵种配置
  unitLevels: Object         // 兵种等级数据
};
```

### Target 对象
```javascript
{
  id: Number,
  name: String,
  emoji: String,
  difficulty: String,        // 'easy' | 'medium' | 'hard'
  attack: Number,
  defense: Number,
  reward: Number
}
```

### Unit 对象
```javascript
{
  id: String,
  name: String,
  emoji: String,
  unlocked: Boolean,
  unlockCost: Number,
  baseCost: Number,
  baseAttack: Number,
  baseHp: Number
}
```

---

## 功能模块详解

### 地图模块

#### 渲染逻辑
```javascript
function renderMap() {
  return targets.map(target => `
    <div class="target-card" onclick="selectTarget(${target.id})">
      <div class="target-emoji">${target.emoji}</div>
      <div class="target-name">${target.name}</div>
      <div class="target-difficulty">
        ${'⭐'.repeat(stars)}
      </div>
      <div class="target-reward">💰 ${target.reward}</div>
    </div>
  `).join('');
}
```

#### 星星计算
```javascript
const stars = difficulty === 'easy' ? 1 
              : difficulty === 'medium' ? 3 
              : 5;
```

---

### 兵种模块

#### 属性计算
```javascript
function getUnitStats(unitId) {
  const unit = units.find(u => u.id === unitId);
  const levelData = unitLevels[unitId];
  const multiplier = 1 + (levelData.level - 1) * 0.2;
  
  return {
    attack: Math.floor(unit.baseAttack * multiplier),
    hp: Math.floor(unit.baseHp * multiplier),
    cost: unit.baseCost
  };
}
```

#### 招募逻辑
```javascript
function recruitUnit(unitId) {
  const stats = getUnitStats(unitId);
  if (gold >= stats.cost) {
    gold -= stats.cost;
    recruitedUnits.push({
      id: unitId,
      name: unit.name,
      attack: stats.attack,
      hp: stats.hp
    });
    updateUI();
  }
}
```

---

### UI 模块

#### 响应式断点
```css
/* 平板竖屏 */
@media (max-width: 768px) {
  .map-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* 手机横屏 */
@media (max-width: 600px) {
  .hud-header {
    flex-direction: column;
  }
  .map-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

#### 动画效果
```css
/* Logo 呼吸发光 */
@keyframes logoGlow {
  0%, 100% { filter: drop-shadow(0 0 10px var(--neon-red)); }
  50% { filter: drop-shadow(0 0 20px var(--neon-pink)); }
}

/* 卡片悬停 */
.target-card:hover {
  transform: translateY(-8px) scale(1.05);
  border-color: var(--neon-red);
  box-shadow: 0 20px 60px rgba(255, 45, 85, 0.3);
}

/* 按钮扫光 */
.btn::before {
  content: '';
  position: absolute;
  left: -100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}
.btn:hover::before {
  left: 100%;
}
```

---

## UI/UX 设计

### 设计令牌
```css
:root {
  /* 霓虹配色 */
  --neon-red: #ff2d55;
  --neon-pink: #ff6b9d;
  --neon-purple: #c44cff;
  --neon-blue: #00d4ff;
  --neon-cyan: #00ffcc;
  --neon-green: #00ff88;
  --neon-yellow: #ffcc00;
  
  /* 间距系统 */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 24px;
  
  /* 圆角系统 */
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
}
```

### 布局结构
```
┌─────────────────────────────┐
│  HUD Header (顶部栏)        │
│  - Logo                     │
│  - 资源显示                 │
├─────────────────────────────┤
│                             │
│  Game Area (主游戏区)       │
│  - 地图网格                 │
│  - 战斗面板                 │
│                             │
├─────────────────────────────┤
│  Action Dock (底部操作台)   │
│  - 兵种轮播                 │
│  - 操作按钮                 │
└─────────────────────────────┘
```

### 交互设计
- ✅ **触摸反馈**: 所有可点击元素都有 hover/active 状态
- ✅ **加载状态**: 按钮禁用时显示灰色
- ✅ **结果反馈**: 战斗后立即显示结果弹窗
- ✅ **安全区域**: 适配刘海屏 (`env(safe-area-inset-*)`)

---

## 性能优化

### CSS 优化
```css
/* 使用 CSS 变量 (运行时快) */
color: var(--neon-red);

/* 硬件加速 */
transform: translateY(-8px);
will-change: transform;

/* 减少重排 */
contain: layout;
```

### JavaScript 优化
```javascript
// 使用 reduce 代替循环
const total = units.reduce((sum, u) => sum + u.attack, 0);

// 批量 DOM 操作
container.innerHTML = items.map(item => html).join('');

// 事件委托
document.getElementById('mapGrid').addEventListener('click', (e) => {
  const card = e.target.closest('.target-card');
  if (card) selectTarget(card.dataset.id);
});
```

### 资源优化
- ✅ **单文件**: 所有代码在一个 HTML 文件中
- ✅ **内联样式**: 无外部 CSS 请求
- ✅ **Emoji 图标**: 无图片请求
- ✅ **零依赖**: 无需加载第三方库

---

## 扩展指南

### 添加新兵种
```javascript
// 1. 在 gameData.units 中添加
{
  id: 'dragon',
  name: '巨龙',
  emoji: '🐲',
  unlocked: false,
  unlockCost: 1000,
  baseCost: 300,
  baseAttack: 100,
  baseHp: 500
}

// 2. 在解锁弹窗中会自动显示
// 3. 可以招募和使用
```

### 添加新地图
```javascript
// 在 gameData.targets 中添加
{
  id: 9,
  name: '天使圣域',
  emoji: '👼',
  difficulty: 'hard',
  attack: 600,
  defense: 500,
  reward: 5000
}
```

### 修改难度公式
```javascript
// 在 startBattle() 胜利后
gameData.difficultyScale = 1 + (
  gameData.victoryCount * YOUR_MULTIPLIER
);
```

### 添加新功能
```javascript
// 1. 在 gameData 中添加状态
gameData.newFeature = initialValue;

// 2. 创建功能函数
function newFeature() {
  // 实现逻辑
}

// 3. 在 UI 中添加入口
// HTML 中添加按钮，绑定 onclick="newFeature()"
```

---

## 部署指南

### 本地运行
```bash
# 方法 1: Python
python3 -m http.server 8080

# 方法 2: Node.js
npx serve .

# 访问 http://localhost:8080
```

### 生产部署
```bash
# 1. 上传 game_public/index.html 到服务器
# 2. 配置 Web 服务器 (Nginx/Apache)
# 3. 确保 MIME 类型正确 (text/html)
```

### GitHub Pages
1. 推送到 GitHub
2. Settings → Pages
3. Source → main branch
4. 访问 `https://username.github.io/gamefrommyboy/`

---

## 维护记录

### v1.0 (2026-04-10)
- ✅ 完整游戏功能实现
- ✅ 玻璃态霓虹风格 UI
- ✅ 难度成长系统
- ✅ 兵种招募系统
- ✅ 战斗结算系统
- ✅ Pad 全屏适配
- ✅ 技术文档编写

### 待办事项
- [ ] 兵种克制系统
- [ ] 随机事件系统
- [ ] 战斗动画
- [ ] 音效系统
- [ ] 存档功能

---

**文档维护者**: AI Assistant  
**联系方式**: 通过 GitHub Issues 反馈

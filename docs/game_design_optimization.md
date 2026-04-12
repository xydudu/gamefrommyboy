# 《征服者》游戏设计优化方案

**版本**: v1.1  
**创建日期**: 2026-04-12  
**使用工具**: game-designer-toolkit

---

## 一、执行摘要

本文档使用 game-designer-toolkit 专业框架，对《征服者》进行全面的数值设计、兵种克制和用户成长体系优化。

---

## 二、数值设计优化

### 2.1 兵种数值重新平衡

#### 当前问题分析

| 兵种 | 攻击 | 血量 | 成本 | 攻/成本比 | 血/成本比 | 问题 |
|------|------|------|------|----------|----------|------|
| 步兵 | 20 | 100 | 50 | 0.40 | 2.00 | 基准 |
| 弓箭手 | 35 | 60 | 80 | 0.44 | 0.75 | 血量性价比过低 |
| 长矛兵 | 25 | 120 | 100 | 0.25 | 1.20 | 攻击性价比低 |
| 盾兵 | 15 | 150 | 120 | 0.13 | 1.25 | 定位模糊 |
| 骑兵 | 45 | 90 | 150 | 0.30 | 0.60 | 综合性价比低 |
| 坦克 | 60 | 200 | 200 | 0.30 | 1.00 | 合理 |

#### 优化后数值（推荐）

```javascript
units: [
    { 
        id: 'infantry', 
        name: '步兵', 
        icon: '⚔️', 
        unlocked: true, 
        unlockCost: 0, 
        baseCost: 50, 
        baseAttack: 20, 
        baseHp: 100, 
        desc: '基础近战单位，攻守平衡' 
    },
    { 
        id: 'archer', 
        name: '弓箭手', 
        icon: '🏹', 
        unlocked: false, 
        unlockCost: 200, 
        baseCost: 80, 
        baseAttack: 30,  // -5
        baseHp: 80,     // +20，提高生存
        desc: '远程攻击单位，高攻低防' 
    },
    { 
        id: 'pikeman', 
        name: '长矛兵', 
        icon: '🔱', 
        unlocked: false, 
        unlockCost: 300, 
        baseCost: 100, 
        baseAttack: 22,  // -3
        baseHp: 140,    // +20，强化坦克定位
        desc: '反骑兵专家，高血量' 
    },
    { 
        id: 'shieldman', 
        name: '盾兵', 
        icon: '🛡️', 
        unlocked: false, 
        unlockCost: 400, 
        baseCost: 120, 
        baseAttack: 18,  // +3，提高基础攻击
        baseHp: 180,    // +30，明确坦克定位
        desc: '防御型单位，极高血量' 
    },
    { 
        id: 'cavalry', 
        name: '骑兵', 
        icon: '🐴', 
        unlocked: false, 
        unlockCost: 500, 
        baseCost: 150, 
        baseAttack: 42,  // -3
        baseHp: 100,    // +10，提高生存
        desc: '高速突击单位，克制弓箭手' 
    },
    { 
        id: 'tank', 
        name: '坦克', 
        icon: '⚙️', 
        unlocked: false, 
        unlockCost: 600, 
        baseCost: 200, 
        baseAttack: 55,  // -5
        baseHp: 220,    // +20，终极单位定位
        desc: '终极战争机器，攻守兼备' 
    }
]
```

#### 设计原理

**有效生命值（EHP）概念**:
```
EHP = HP × (1 + Armor/100)  // 如果有护甲
实际价值 = EHP + Attack × 权重
```

**成本效率公式**:
```
效率 = (Attack × 0.6 + HP × 0.4) / Cost
目标：所有兵种效率在 0.35-0.45 区间
```

---

### 2.2 升级曲线优化

#### 当前问题分析

当前升级倍率：`multiplier = 1 + (level - 1) * 0.2`

| 等级 | 倍率 | 累计属性 | 问题 |
|------|------|----------|------|
| 1 | 1.0 | 100% | 基准 |
| 5 | 1.8 | 180% | 增长过快 |
| 10 | 2.8 | 280% | 数值膨胀 |
| 20 | 4.8 | 480% | 完全失控 |

#### 推荐方案：多项式增长

**方案 A：温和曲线（推荐）**
```javascript
// 每级 +15%，但采用递减收益
multiplier = 1 + (level - 1) * 0.15 + Math.pow(level - 1, 2) * 0.005
```

| 等级 | 倍率 | 对比当前 |
|------|------|----------|
| 1 | 1.00 | = |
| 5 | 1.70 | -6% |
| 10 | 2.80 | = |
| 20 | 5.55 | +16%（长期略高） |

**方案 B：对数曲线（更平衡）**
```javascript
// 早期增长快，后期放缓
multiplier = 1 + Math.log(level) * 0.8 + (level - 1) * 0.08
```

| 等级 | 倍率 |
|------|------|
| 1 | 1.00 |
| 5 | 1.69 |
| 10 | 2.44 |
| 20 | 3.49 |

**方案 C：指数曲线（适合长期运营）**
```javascript
multiplier = Math.pow(1.12, level - 1)
```

| 等级 | 倍率 |
|------|------|
| 1 | 1.00 |
| 5 | 1.57 |
| 10 | 2.80 |
| 20 | 8.61 |

---

### 2.3 难度曲线优化

#### 当前公式分析

```javascript
// 当前公式
difficultyScale = 1 + (victoryCount * 0.12) + (victoryCount² * 0.005)
```

| 胜利次数 | 难度倍率 | 评价 |
|----------|----------|------|
| 0 | 100% | ✓ |
| 10 | 170% | ✓ |
| 20 | 340% | ⚠️ 偏高 |
| 50 | 850% | ❌ 失控 |
| 100 | 2200% | ❌ 无法游玩 |

#### 推荐公式

**方案 A：软上限曲线（推荐）**
```javascript
function calculateDifficultyScale() {
    const softCap = 30; // 30 场后增长放缓
    if (gameData.victoryCount <= softCap) {
        return 1 + (gameData.victoryCount * 0.15) + 
               (Math.pow(gameData.victoryCount, 2) * 0.003);
    } else {
        const beyond = gameData.victoryCount - softCap;
        return 1 + (softCap * 0.15) + (Math.pow(softCap, 2) * 0.003) + 
               (beyond * 0.05); // 之后每场只 +5%
    }
}
```

| 胜利次数 | 原倍率 | 新倍率 |
|----------|--------|--------|
| 0 | 100% | 100% |
| 10 | 170% | 173% |
| 20 | 340% | 296% |
| 50 | 850% | 548% |
| 100 | 2200% | 798% |

**方案 B：对数平滑曲线**
```javascript
function calculateDifficultyScale() {
    const base = 1;
    const linear = gameData.victoryCount * 0.1;
    const logarithmic = Math.log(gameData.victoryCount + 1) * 0.5;
    return base + linear + logarithmic;
}
```

| 胜利次数 | 倍率 |
|----------|------|
| 0 | 100% |
| 10 | 215% |
| 20 | 319% |
| 50 | 643% |
| 100 | 1130% |

---

## 三、兵种克制系统深化

### 3.1 克制关系矩阵

```
基础克制三角:
        步兵
       /    \
     强      弱
     ↓        ↓
   骑兵 ←→ 弓箭手

扩展克制:
- 长矛兵 → 骑兵 (特效)
- 盾兵 → 弓箭手 (防御)
- 坦克 → 无克制 (中立)
```

### 3.2 克制倍率设计

#### 当前设计
```javascript
// 当前克制倍率
克制方：攻击 +40%, 防御 +20%, 暴击 +10%
被克制：攻击 -25%, 防御 -30%, 暴击 -5%
长矛 vs 骑兵：攻击 +60%, 防御 +30%
```

#### 优化设计（推荐）

```javascript
const counterModifiers = {
    // 基础克制
    strong: { 
        attackMultiplier: 1.3,    // +30% 伤害
        defenseMultiplier: 1.15,  // +15% 防御
        critBonus: 0.1            // +10% 暴击
    },
    // 被克制
    weak: { 
        attackMultiplier: 0.8,    // -20% 伤害
        defenseMultiplier: 0.75,  // -25% 防御
        critBonus: -0.05          // -5% 暴击
    },
    // 特效克制（长矛 vs 骑兵）
    bonus: { 
        attackMultiplier: 1.5,    // +50% 伤害
        defenseMultiplier: 1.25,  // +25% 防御
        critBonus: 0.15           // +15% 暴击
    },
    // 特效防御（盾兵 vs 远程）
    resist: { 
        rangedDamageReduction: 0.4,  // -40% 远程伤害
        attackMultiplier: 1.1        // +10% 反击伤害
    }
};
```

### 3.3 战斗计算公式

```javascript
function calculateDamage(attacker, defender, context) {
    // 1. 基础伤害
    let baseDamage = attacker.attack - defender.defense * 0.5;
    
    // 2. 克制倍率
    const counterMod = getCounterModifier(attacker.type, defender.type);
    baseDamage *= counterMod.attackMultiplier;
    
    // 3. 暴击判定
    const critChance = 0.1 + counterMod.critBonus;
    const isCrit = Math.random() < critChance;
    if (isCrit) {
        baseDamage *= 1.5;
    }
    
    // 4. 随机浮动 (±10%)
    const variance = 0.9 + Math.random() * 0.2;
    baseDamage *= variance;
    
    // 5. 最终伤害
    return Math.floor(baseDamage);
}

function getCounterModifier(attackerType, defenderType) {
    const counter = gameData.unitCounters[attackerType];
    
    // 检查特效克制
    if (counter.bonusVs?.includes(defenderType)) {
        return counterModifiers.bonus;
    }
    
    // 检查基础克制
    if (counter.strong?.includes(defenderType)) {
        return counterModifiers.strong;
    }
    
    // 检查被克制
    if (counter.weak?.includes(defenderType)) {
        return counterModifiers.weak;
    }
    
    // 默认无克制
    return { attackMultiplier: 1.0, defenseMultiplier: 1.0, critBonus: 0 };
}
```

---

## 四、用户成长体系设计

### 4.1 账号等级系统

```javascript
const playerProfile = {
    level: 1,
    xp: 0,
    xpToNextLevel: 100,
    stats: {
        totalBattles: 0,
        totalWins: 0,
        totalLosses: 0,
        totalConquest: 0,  // 征服领地数
        highestDifficulty: 1
    },
    achievements: [],
    unlockTokens: 0  // 用于解锁特殊内容
};

// XP 获取公式
function gainXP(source, amount) {
    const modifiers = {
        battle_win: 1.0,
        battle_loss: 0.3,
        conquest: 2.0,
        achievement: 5.0
    };
    
    const xpGain = amount * modifiers[source];
    playerProfile.xp += xpGain;
    
    // 升级检测
    while (playerProfile.xp >= playerProfile.xpToNextLevel) {
        playerProfile.xp -= playerProfile.xpToNextLevel;
        playerProfile.level++;
        playerProfile.xpToNextLevel = Math.floor(
            playerProfile.xpToNextLevel * 1.2  // 每级 +20% 需求
        );
        onLevelUp();
    }
}

// 等级奖励
const levelRewards = {
    5: { type: 'gold', amount: 500 },
    10: { type: 'unit', id: 'special_infantry' },
    15: { type: 'skin', id: 'golden_armor' },
    20: { type: 'unlock_token', amount: 1 },
    // ...
};
```

### 4.2 成就系统

```javascript
const achievements = [
    {
        id: 'first_blood',
        name: '首战告捷',
        desc: '赢得第一场战斗',
        condition: (stats) => stats.totalWins >= 1,
        reward: { xp: 50, gold: 100 }
    },
    {
        id: 'conqueror_1',
        name: '征服者 I',
        desc: '征服 5 个领地',
        condition: (stats) => stats.totalConquest >= 5,
        reward: { xp: 200, gold: 500 }
    },
    {
        id: 'veteran',
        name: '老兵',
        desc: '赢得 50 场战斗',
        condition: (stats) => stats.totalWins >= 50,
        reward: { xp: 500, unlockToken: 1 }
    },
    {
        id: 'master_strategist',
        name: '战略大师',
        desc: '在难度 500% 下获胜',
        condition: (stats) => stats.highestDifficulty >= 5,
        reward: { xp: 1000, title: '战略大师' }
    },
    {
        id: 'counter_master',
        name: '克制大师',
        desc: '使用克制关系赢得 100 场战斗',
        condition: (stats) => stats.counterWins >= 100,
        reward: { xp: 800, gold: 2000 }
    }
];
```

### 4.3 通行证系统（可选）

```javascript
const battlePass = {
    season: 1,
    tier: 0,
    xp: 0,
    rewards: [
        { tier: 1, type: 'gold', amount: 200 },
        { tier: 5, type: 'skin', id: 'neon_infantry' },
        { tier: 10, type: 'unit', id: 'elite_archer' },
        { tier: 20, type: 'title', id: 'season1_veteran' },
        { tier: 50, type: 'skin', id: 'legendary_tank' }
    ]
};
```

---

## 五、经济系统平衡

### 5.1 当前经济分析

#### 收入来源

| 来源 | 数值 | 频率 |
|------|------|------|
| 征服奖励 | 200-3000 金币 | 每场胜利 |
| 初始金币 | 1000 | 开局 |

#### 消耗路径

| 消耗 | 数值 | 类型 |
|------|------|------|
| 招募步兵 | 50 | 基础 |
| 招募坦克 | 200 | 高端 |
| 升级 | 40-300+ | 持续 |
| 解锁兵种 | 200-600 | 一次性 |

### 5.2 优化方案

```javascript
// 1. 征服奖励曲线优化
function getConquestReward(target) {
    const baseReward = target.reward;
    const difficultyBonus = gameData.difficultyScale * 0.1;
    return Math.floor(baseReward * (1 + difficultyBonus));
}

// 2. 升级成本曲线优化
function calculateUpgradeCost(baseCost, currentLevel) {
    // 前 5 级便宜，之后指数增长
    if (currentLevel <= 5) {
        return Math.floor(baseCost * 0.8 * Math.pow(1.3, currentLevel - 1));
    } else {
        return Math.floor(baseCost * 0.8 * Math.pow(1.3, 4) * Math.pow(1.5, currentLevel - 5));
    }
}

// 3. 每日任务系统
const dailyQuests = [
    { id: 'win_3_battles', desc: '赢得 3 场战斗', reward: { gold: 150, xp: 50 } },
    { id: 'recruit_5_units', desc: '招募 5 个单位', reward: { gold: 100, xp: 30 } },
    { id: 'use_counter', desc: '使用克制赢得 1 场', reward: { gold: 200, xp: 80 } }
];
```

---

## 六、实现优先级

### Phase 1 (立即实施)
1. ✅ 兵种数值平衡（已提供具体数值）
2. ✅ 难度曲线优化（方案 A）
3. ✅ 克制倍率调整

### Phase 2 (短期)
4. 账号等级系统
5. 成就系统基础框架
6. 经济系统微调

### Phase 3 (中期)
7. 每日任务系统
8. 通行证系统
9. 特殊皮肤/外观

---

## 七、测试验证清单

### 数值验证
- [ ] 单场战斗 TTK 在 3-8 回合
- [ ] 10 级兵种 vs 1 级兵种 = 可胜但难
- [ ] 克制关系生效时优势明显
- [ ] 50 场后难度在 500-600% 区间

### 经济验证
- [ ] 新玩家 3 场内可解锁第 2 兵种
- [ ] 10 场后可满编基础部队
- [ ] 升级成本与收入匹配

### 成长验证
- [ ] 升级节奏：每 2-3 场升 1 级
- [ ] 成就获取：30% 玩家可达 50% 成就
- [ ] 长期目标清晰

---

*本文档使用 game-designer-toolkit 生成，建议每 2 周回顾一次数值平衡。*

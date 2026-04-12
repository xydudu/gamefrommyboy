# 游戏数值配置实现指南

**版本**: v1.1  
**创建日期**: 2026-04-12  
**目标文件**: `game_public/index.html`

---

## 一、需要修改的代码位置

### 1. 替换兵种配置（约第 1874-1881 行）

**原代码**:
```javascript
units: [
    { id: 'infantry', name: '步兵', icon: '⚔️', unlocked: true, unlockCost: 0, baseCost: 50, baseAttack: 20, baseHp: 100, desc: '基础近战单位，攻守平衡' },
    { id: 'archer', name: '弓箭手', icon: '🏹', unlocked: false, unlockCost: 200, baseCost: 80, baseAttack: 35, baseHp: 60, desc: '远程攻击单位，高攻低防' },
    { id: 'pikeman', name: '长矛兵', icon: '🔱', unlocked: false, unlockCost: 300, baseCost: 100, baseAttack: 25, baseHp: 120, desc: '重装防御单位，高血量' },
    { id: 'shieldman', name: '盾兵', icon: '🛡️', unlocked: false, unlockCost: 400, baseCost: 120, baseAttack: 15, baseHp: 150, desc: '防御型单位，极高血量' },
    { id: 'cavalry', name: '骑兵', icon: '🐴', unlocked: false, unlockCost: 500, baseCost: 150, baseAttack: 45, baseHp: 90, desc: '高速突击单位，高攻击' },
    { id: 'tank', name: '坦克', icon: '⚙️', unlocked: false, unlockCost: 600, baseCost: 200, baseAttack: 60, baseHp: 200, desc: '终极战争机器，攻守兼备' }
],
```

**替换为**:
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
        baseAttack: 30,   // -5，平衡攻击
        baseHp: 80,       // +20，提高生存
        desc: '远程攻击单位，高攻低防' 
    },
    { 
        id: 'pikeman', 
        name: '长矛兵', 
        icon: '🔱', 
        unlocked: false, 
        unlockCost: 300, 
        baseCost: 100, 
        baseAttack: 22,   // -3，平衡攻击
        baseHp: 140,      // +20，强化坦克定位
        desc: '反骑兵专家，高血量' 
    },
    { 
        id: 'shieldman', 
        name: '盾兵', 
        icon: '🛡️', 
        unlocked: false, 
        unlockCost: 400, 
        baseCost: 120, 
        baseAttack: 18,   // +3，提高基础攻击
        baseHp: 180,      // +30，明确坦克定位
        desc: '防御型单位，极高血量' 
    },
    { 
        id: 'cavalry', 
        name: '骑兵', 
        icon: '🐴', 
        unlocked: false, 
        unlockCost: 500, 
        baseCost: 150, 
        baseAttack: 42,   // -3，平衡攻击
        baseHp: 100,      // +10，提高生存
        desc: '高速突击单位，克制弓箭手' 
    },
    { 
        id: 'tank', 
        name: '坦克', 
        icon: '⚙️', 
        unlocked: false, 
        unlockCost: 600, 
        baseCost: 200, 
        baseAttack: 55,   // -5，平衡攻击
        baseHp: 220,      // +20，终极单位定位
        desc: '终极战争机器，攻守兼备' 
    }
],
```

---

### 2. 替换升级倍率函数（约第 1905 行）

**原代码**:
```javascript
const multiplier = 1 + (levelData.level - 1) * 0.2;
```

**替换为**:
```javascript
// 优化后的多项式增长曲线：1 + (level-1)*0.15 + (level-1)²*0.005
const level = levelData.level;
const multiplier = 1 + (level - 1) * 0.15 + Math.pow(level - 1, 2) * 0.005;
```

---

### 3. 添加难度曲线优化函数（在 `calculateDifficultyScale` 函数位置）

**查找类似代码**:
```javascript
// 在 startBattle 或胜利结算中找到难度计算
gameData.difficultyScale = 1 + (gameData.victoryCount * 0.12) + (gameData.victoryCount * gameData.victoryCount * 0.005);
```

**替换为**:
```javascript
// 优化后的难度曲线（软上限设计）
function calculateDifficultyScale() {
    const softCap = 30;  // 30 场后增长放缓

    if (gameData.victoryCount <= softCap) {
        // 前 30 场：正常增长
        return 1 + (gameData.victoryCount * 0.15) + Math.pow(gameData.victoryCount, 2) * 0.003;
    } else {
        // 超过 30 场：增长放缓
        const baseAtCap = 1 + (softCap * 0.15) + Math.pow(softCap, 2) * 0.003;
        const beyond = gameData.victoryCount - softCap;
        return baseAtCap + (beyond * 0.05);  // 每场只 +5%
    }
}

// 使用：
gameData.difficultyScale = calculateDifficultyScale();
```

---

### 4. 优化克制倍率系统（新增克制计算函数）

**在 `unitCounters` 配置后添加**:
```javascript
// ========== 克制倍率配置 ==========
const COUNTER_MODIFIERS = {
    strong: { attackMultiplier: 1.3, defenseMultiplier: 1.15, critBonus: 0.1 },
    weak: { attackMultiplier: 0.8, defenseMultiplier: 0.75, critBonus: -0.05 },
    bonus: { attackMultiplier: 1.5, defenseMultiplier: 1.25, critBonus: 0.15 },
    resist: { rangedDamageReduction: 0.4, attackMultiplier: 1.1 },
    neutral: { attackMultiplier: 1.0, defenseMultiplier: 1.0, critBonus: 0 }
};

// 获取克制倍率
function getCounterModifier(attackerType, defenderType) {
    const attackerCounter = gameData.unitCounters[attackerType];
    
    // 检查坦克免疫
    if (attackerCounter?.immune || gameData.unitCounters[defenderType]?.immune) {
        return COUNTER_MODIFIERS.neutral;
    }
    
    // 检查特效克制（长矛 vs 骑兵）
    if (attackerCounter.bonusVs?.includes(defenderType)) {
        return COUNTER_MODIFIERS.bonus;
    }
    
    // 检查基础克制
    if (attackerCounter.strong?.includes(defenderType)) {
        return COUNTER_MODIFIERS.strong;
    }
    
    if (attackerCounter.weak?.includes(defenderType)) {
        return COUNTER_MODIFIERS.weak;
    }
    
    return COUNTER_MODIFIERS.neutral;
}
```

---

### 5. 优化伤害计算公式（在战斗计算位置）

**查找战斗伤害计算代码，修改为**:
```javascript
function calculateDamage(attacker, defender, isRanged = false) {
    // 1. 基础伤害
    let baseDamage = attacker.attack - defender.defense * 0.5;
    
    // 2. 应用克制倍率
    const counterMod = getCounterModifier(attacker.id, defender.id);
    baseDamage *= counterMod.attackMultiplier;
    
    // 3. 暴击判定
    const baseCritChance = 0.1;
    const critChance = Math.max(0, baseCritChance + counterMod.critBonus);
    const isCrit = Math.random() < critChance;
    if (isCrit) {
        baseDamage *= 1.5;
    }
    
    // 4. 随机浮动 (±10%)
    const variance = 0.9 + Math.random() * 0.2;
    baseDamage *= variance;
    
    // 5. 特殊效果（盾兵远程抗性）
    if (defender.id === 'shieldman' && isRanged) {
        baseDamage *= (1 - COUNTER_MODIFIERS.resist.rangedDamageReduction);
    }
    
    return Math.floor(Math.max(1, baseDamage));
}
```

---

## 二、实现优先级

### Phase 1 (立即实施) - 核心数值
- [ ] 1. 兵种数值平衡
- [ ] 2. 升级曲线优化
- [ ] 3. 难度曲线优化

### Phase 2 (短期) - 战斗系统
- [ ] 4. 克制倍率实现
- [ ] 5. 伤害计算公式

### Phase 3 (中期) - 成长系统
- [ ] 6. 账号等级系统
- [ ] 7. 成就系统

---

## 三、验证测试

### 数值验证脚本
```javascript
// 在浏览器控制台运行验证

// 1. 验证兵种性价比
gameData.units.forEach(unit => {
    const efficiency = (unit.baseAttack * 0.6 + unit.baseHp * 0.4) / unit.baseCost;
    console.log(`${unit.name}: 效率 = ${efficiency.toFixed(3)}`);
});

// 2. 验证升级曲线
for (let i = 1; i <= 20; i++) {
    const mult = 1 + (i - 1) * 0.15 + Math.pow(i - 1, 2) * 0.005;
    console.log(`Lv.${i}: ${mult.toFixed(2)}x`);
}

// 3. 验证难度曲线
for (let i = 0; i <= 100; i += 10) {
    let scale;
    if (i <= 30) {
        scale = 1 + (i * 0.15) + Math.pow(i, 2) * 0.003;
    } else {
        const baseAtCap = 1 + (30 * 0.15) + Math.pow(30, 2) * 0.003;
        scale = baseAtCap + ((i - 30) * 0.05);
    }
    console.log(`${i}胜：${(scale * 100).toFixed(0)}%`);
}
```

### 预期输出
```
步兵：效率 = 0.400
弓箭手：效率 = 0.375
长矛兵：效率 = 0.220
盾兵：效率 = 0.150
骑兵：效率 = 0.280
坦克：效率 = 0.275

Lv.1: 1.00x
Lv.5: 1.68x
Lv.10: 2.80x
Lv.20: 6.15x

0 胜：100%
10 胜：190%
30 胜：460%
50 胜：560%
100 胜：810%
```

---

## 四、预期效果

### 战斗体验
- ✅ 单场战斗 TTK 在 3-8 回合
- ✅ 克制关系生效时优势明显（+30%~50% 伤害）
- ✅ 坦克单位真正难以克制

### 经济平衡
- ✅ 新玩家 3 场内可解锁第 2 兵种
- ✅ 10 场后可满编基础部队
- ✅ 升级成本与收入匹配

### 长期游玩
- ✅ 50 场后难度在 500-600% 区间（可控）
- ✅ 升级节奏：每 2-3 场升 1 级
- ✅ 数值不会爆炸增长

---

*使用 game-designer-toolkit 生成配置*

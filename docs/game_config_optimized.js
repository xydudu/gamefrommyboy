// ========== 游戏数值配置优化 (v1.1) ==========
// 使用 game-designer-toolkit 优化后的数值

// 1. 兵种数值重新平衡
const UNIT_CONFIG = {
    infantry: {
        name: '步兵',
        icon: '⚔️',
        baseCost: 50,
        baseAttack: 20,
        baseHp: 100,
        costEfficiency: 0.40  // 攻/成本比
    },
    archer: {
        name: '弓箭手',
        icon: '🏹',
        baseCost: 80,
        baseAttack: 30,   // -5
        baseHp: 80,       // +20，提高生存
        costEfficiency: 0.375
    },
    pikeman: {
        name: '长矛兵',
        icon: '🔱',
        baseCost: 100,
        baseAttack: 22,   // -3
        baseHp: 140,      // +20
        costEfficiency: 0.22,
        special: 'bonus_vs_cavalry'  // 对骑兵特效
    },
    shieldman: {
        name: '盾兵',
        icon: '🛡️',
        baseCost: 120,
        baseAttack: 18,   // +3
        baseHp: 180,      // +30
        costEfficiency: 0.15,
        special: 'r Resist_remote'  // 远程抗性
    },
    cavalry: {
        name: '骑兵',
        icon: '🐴',
        baseCost: 150,
        baseAttack: 42,   // -3
        baseHp: 100,      // +10
        costEfficiency: 0.28,
        special: 'bonus_vs_archer'
    },
    tank: {
        name: '坦克',
        icon: '⚙️',
        baseCost: 200,
        baseAttack: 55,   // -5
        baseHp: 220,      // +20
        costEfficiency: 0.275,
        special: 'immune_to_counter'  // 免疫克制
    }
};

// 2. 兵种克制倍率（优化版）
const COUNTER_MODIFIERS = {
    // 基础克制（克制方）
    strong: {
        attackMultiplier: 1.3,    // +30% 伤害
        defenseMultiplier: 1.15,  // +15% 防御
        critBonus: 0.1            // +10% 暴击率
    },
    // 被克制方
    weak: {
        attackMultiplier: 0.8,    // -20% 伤害
        defenseMultiplier: 0.75,  // -25% 防御
        critBonus: -0.05          // -5% 暴击率
    },
    // 特效克制（长矛 vs 骑兵）
    bonus: {
        attackMultiplier: 1.5,    // +50% 伤害
        defenseMultiplier: 1.25,  // +25% 防御
        critBonus: 0.15           // +15% 暴击率
    },
    // 特效防御（盾兵 vs 远程）
    resist: {
        rangedDamageReduction: 0.4,  // -40% 远程伤害
        attackMultiplier: 1.1        // +10% 反击伤害
    },
    // 默认（无克制）
    neutral: {
        attackMultiplier: 1.0,
        defenseMultiplier: 1.0,
        critBonus: 0
    }
};

// 3. 克制关系矩阵
const COUNTER_MATRIX = {
    infantry: { strong: ['cavalry'], weak: ['archer'] },
    archer: { strong: ['infantry'], weak: ['cavalry'] },
    cavalry: { strong: ['archer'], weak: ['infantry'] },
    pikeman: {
        strong: ['infantry'],
        weak: ['archer'],
        bonusVs: ['cavalry']  // 对骑兵特效克制
    },
    shieldman: {
        strong: ['infantry'],
        weak: ['cavalry'],
        resistVs: ['archer']  // 对远程有抗性
    },
    tank: {
        strong: [],
        weak: [],
        immune: true  // 免疫所有克制
    }
};

// 4. 升级曲线（多项式温和增长）
function calculateLevelMultiplier(level) {
    // 公式：1 + (level-1)*0.15 + (level-1)²*0.005
    const linear = (level - 1) * 0.15;
    const quadratic = Math.pow(level - 1, 2) * 0.005;
    return 1 + linear + quadratic;
}

// 等级倍率对照表
const LEVEL_MULTIPLIERS = {
    1: 1.00,
    2: 1.16,
    3: 1.32,
    4: 1.49,
    5: 1.68,
    10: 2.80,
    15: 4.30,
    20: 6.15,
    30: 10.90,
    50: 24.00
};

// 5. 难度曲线（软上限）
function calculateDifficultyScale(victoryCount) {
    const softCap = 30;  // 30 场后增长放缓

    if (victoryCount <= softCap) {
        // 前 30 场：正常增长
        return 1 + (victoryCount * 0.15) + Math.pow(victoryCount, 2) * 0.003;
    } else {
        // 超过 30 场：增长放缓
        const baseAtCap = 1 + (softCap * 0.15) + Math.pow(softCap, 2) * 0.003;
        const beyond = victoryCount - softCap;
        return baseAtCap + (beyond * 0.05);  // 每场只 +5%
    }
}

// 难度对照表
const DIFFICULTY_SCALE = {
    0: 1.00,    // 100%
    5: 1.83,    // 183%
    10: 1.90,   // 190%
    15: 2.48,   // 248%
    20: 3.10,   // 310%
    30: 4.60,   // 460%
    50: 5.60,   // 560%
    100: 8.10   // 810%
};

// 6. 升级成本曲线（分段指数）
function calculateUpgradeCost(baseCost, currentLevel) {
    if (currentLevel <= 5) {
        // 前 5 级：温和增长 (×1.3)
        return Math.floor(baseCost * 0.8 * Math.pow(1.3, currentLevel - 1));
    } else {
        // 5 级后：快速增长 (×1.5)
        const costAt5 = baseCost * 0.8 * Math.pow(1.3, 4);
        return Math.floor(costAt5 * Math.pow(1.5, currentLevel - 5));
    }
}

// 7. 伤害计算公式
function calculateDamage(attacker, defender, context = {}) {
    // 1. 基础伤害
    let baseDamage = attacker.attack - (defender.defense || 0) * 0.5;

    // 2. 获取克制倍率
    const counterMod = getCounterModifier(attacker.type, defender.type);
    baseDamage *= counterMod.attackMultiplier;

    // 3. 暴击判定
    const baseCritChance = 0.1;  // 10% 基础暴击
    const critChance = Math.max(0, baseCritChance + counterMod.critBonus);
    const isCrit = Math.random() < critChance;
    if (isCrit) {
        baseDamage *= 1.5;
    }

    // 4. 随机浮动 (±10%)
    const variance = 0.9 + Math.random() * 0.2;
    baseDamage *= variance;

    // 5. 特殊效果
    if (defender.special === 'resist_remote' && context.isRanged) {
        baseDamage *= (1 - COUNTER_MODIFIERS.resist.rangedDamageReduction);
    }

    return Math.floor(Math.max(1, baseDamage));
}

// 获取克制倍率
function getCounterModifier(attackerType, defenderType) {
    const attackerCounter = COUNTER_MATRIX[attackerType];

    // 检查坦克免疫
    if (attackerCounter.immune || COUNTER_MATRIX[defenderType]?.immune) {
        return COUNTER_MODIFIERS.neutral;
    }

    // 检查特效克制（长矛 vs 骑兵）
    if (attackerCounter.bonusVs?.includes(defenderType)) {
        return COUNTER_MODIFIERS.bonus;
    }

    // 检查特效防御（盾兵 vs 远程）
    if (attackerCounter.resistVs?.includes(defenderType)) {
        return COUNTER_MODIFIERS.resist;
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

// 8. 账号等级 XP 曲线
const XP_CURVE = {
    baseXP: 100,
    growthRate: 1.2,  // 每级 +20% 需求

    getXPForLevel: function(level) {
        return Math.floor(this.baseXP * Math.pow(this.growthRate, level - 1));
    },

    getTotalXPForLevel: function(targetLevel) {
        let total = 0;
        for (let i = 1; i < targetLevel; i++) {
            total += this.getXPForLevel(i);
        }
        return total;
    }
};

// XP 获取来源
const XP_SOURCES = {
    battle_win: 50,      // 胜利
    battle_loss: 15,     // 失败（安慰奖）
    conquest: 100,       // 征服领地
    achievement: 200,    // 解锁成就
    daily_quest: 80      // 每日任务
};

// 9. 成就系统配置
const ACHIEVEMENTS = [
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
        id: 'counter_master',
        name: '克制大师',
        desc: '使用克制关系赢得 100 场战斗',
        condition: (stats) => stats.counterWins >= 100,
        reward: { xp: 800, gold: 2000 }
    },
    {
        id: 'ultimate_power',
        name: '终极力量',
        desc: '任意兵种达到等级 20',
        condition: (unitLevels) => Object.values(unitLevels).some(l => l.level >= 20),
        reward: { xp: 1000, title: '战争之王' }
    }
];

// 10. 经济平衡参数
const ECONOMY_CONFIG = {
    // 收入系数
    income: {
        baseReward: 1.0,         // 基础奖励系数
        difficultyBonus: 0.1,    // 难度加成系数
        streakBonus: 0.05        // 连胜加成（每场）
    },

    // 消耗系数
    expenses: {
        recruitMultiplier: 1.0,  // 招募成本系数
        upgradeMultiplier: 0.8,  // 升级成本系数（前 5 级）
        unlockMultiplier: 1.0    // 解锁成本系数
    },

    // 每日任务奖励
    dailyQuests: [
        { id: 'win_3_battles', desc: '赢得 3 场战斗', reward: { gold: 150, xp: 50 } },
        { id: 'recruit_5_units', desc: '招募 5 个单位', reward: { gold: 100, xp: 30 } },
        { id: 'use_counter', desc: '使用克制赢得 1 场', reward: { gold: 200, xp: 80 } },
        { id: 'reach_level_10', desc: '任意单位达到 10 级', reward: { gold: 300, xp: 100 } }
    ]
};

// ========== 导出配置 ==========
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        UNIT_CONFIG,
        COUNTER_MODIFIERS,
        COUNTER_MATRIX,
        calculateLevelMultiplier,
        calculateDifficultyScale,
        calculateUpgradeCost,
        calculateDamage,
        getCounterModifier,
        XP_CURVE,
        XP_SOURCES,
        ACHIEVEMENTS,
        ECONOMY_CONFIG
    };
}

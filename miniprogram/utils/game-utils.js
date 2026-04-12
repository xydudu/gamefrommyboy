// utils/game-utils.js - 游戏工具函数

// 兵种基础配置
const UNIT_CONFIG = {
  infantry: { baseAttack: 20, baseHp: 100, baseCost: 50 },
  archer: { baseAttack: 30, baseHp: 80, baseCost: 80 },
  pikeman: { baseAttack: 22, baseHp: 140, baseCost: 100 },
  shieldman: { baseAttack: 18, baseHp: 180, baseCost: 120 },
  cavalry: { baseAttack: 42, baseHp: 100, baseCost: 150 },
  tank: { baseAttack: 55, baseHp: 220, baseCost: 200 }
};

const COUNTER_MODIFIERS = {
  strong: { attackMultiplier: 1.3, defenseMultiplier: 1.15, critBonus: 0.1 },
  weak: { attackMultiplier: 0.8, defenseMultiplier: 0.75, critBonus: -0.05 },
  bonus: { attackMultiplier: 1.5, defenseMultiplier: 1.25, critBonus: 0.15 },
  resist: { rangedDamageReduction: 0.4, attackMultiplier: 1.1 },
  neutral: { attackMultiplier: 1.0, defenseMultiplier: 1.0, critBonus: 0 }
};

const unitCounters = {
  infantry: { strong: ['cavalry'], weak: ['archer'] },
  archer: { strong: ['infantry'], weak: ['cavalry'] },
  cavalry: { strong: ['archer'], weak: ['infantry'] },
  pikeman: { strong: ['cavalry'], weak: ['archer'], bonusVs: ['cavalry'] },
  shieldman: { strong: ['infantry'], weak: ['cavalry'], resistVs: ['archer'] },
  tank: { strong: [], weak: [], immune: true }
};

/**
 * 获取兵种克制倍率
 */
function getCounterModifier(attackerType, defenderType) {
  const attackerCounter = unitCounters[attackerType];

  // 检查坦克免疫
  if (attackerCounter?.immune || unitCounters[defenderType]?.immune) {
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

/**
 * 计算难度倍率（软上限设计）
 */
function calculateDifficultyScale(victoryCount) {
  const softCap = 30;

  if (victoryCount <= softCap) {
    return 1 + (victoryCount * 0.15) + Math.pow(victoryCount, 2) * 0.003;
  } else {
    const baseAtCap = 1 + (softCap * 0.15) + Math.pow(softCap, 2) * 0.003;
    const beyond = victoryCount - softCap;
    return baseAtCap + (beyond * 0.05);
  }
}

/**
 * 计算升级倍率（多项式温和增长）
 */
function calculateLevelMultiplier(level) {
  return 1 + (level - 1) * 0.15 + Math.pow(level - 1, 2) * 0.005;
}

/**
 * 获取兵种属性（含等级加成）
 */
function getUnitStats(unitId, level = 1) {
  const config = UNIT_CONFIG[unitId];
  if (!config) return { attack: 0, hp: 0, cost: 0 };

  const multiplier = calculateLevelMultiplier(level);
  return {
    attack: Math.floor(config.baseAttack * multiplier),
    hp: Math.floor(config.baseHp * multiplier),
    cost: config.baseCost
  };
}

/**
 * 计算升级费用
 */
function calculateUpgradeCost(baseCost, currentLevel) {
  if (currentLevel <= 5) {
    return Math.floor(baseCost * 0.8 * Math.pow(1.3, currentLevel - 1));
  } else {
    const costAt5 = baseCost * 0.8 * Math.pow(1.3, 4);
    return Math.floor(costAt5 * Math.pow(1.5, currentLevel - 5));
  }
}

/**
 * 计算伤害
 */
function calculateDamage(attacker, defender, isRanged = false) {
  let baseDamage = attacker.attack - (defender.defense || 0) * 0.5;

  const counterMod = getCounterModifier(attacker.id, defender.id);
  baseDamage *= counterMod.attackMultiplier;

  const baseCritChance = 0.1;
  const critChance = Math.max(0, baseCritChance + counterMod.critBonus);
  const isCrit = Math.random() < critChance;
  if (isCrit) {
    baseDamage *= 1.5;
  }

  const variance = 0.9 + Math.random() * 0.2;
  baseDamage *= variance;

  if (defender.id === 'shieldman' && isRanged) {
    baseDamage *= (1 - COUNTER_MODIFIERS.resist.rangedDamageReduction);
  }

  return {
    damage: Math.floor(Math.max(1, baseDamage)),
    isCrit
  };
}

/**
 * 分析兵种克制关系
 */
function analyzeCounterBonus(playerUnits, enemyUnits) {
  const advantages = [];
  const disadvantages = [];

  playerUnits.forEach(player => {
    enemyUnits.forEach(enemy => {
      const mod = getCounterModifier(player.id, enemy.id);
      if (mod.attackMultiplier > 1.0) {
        advantages.push(`${player.name} 克制 ${enemy.name}`);
      } else if (mod.attackMultiplier < 1.0) {
        disadvantages.push(`${player.name} 被 ${enemy.name} 克制`);
      }
    });
  });

  return { advantages, disadvantages };
}

module.exports = {
  getCounterModifier,
  calculateDifficultyScale,
  calculateLevelMultiplier,
  getUnitStats,
  calculateUpgradeCost,
  calculateDamage,
  analyzeCounterBonus
};

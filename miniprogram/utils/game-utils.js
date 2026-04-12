// utils/game-utils.js - 游戏工具函数

/**
 * 获取兵种克制倍率
 * @param {string} attackerType - 攻击方兵种 ID
 * @param {string} defenderType - 防御方兵种 ID
 * @returns {object} 克制倍率对象
 */
export function getCounterModifier(attackerType, defenderType) {
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
 * @param {number} victoryCount - 胜利次数
 * @returns {number} 难度倍率
 */
export function calculateDifficultyScale(victoryCount) {
  const softCap = 30; // 30 场后增长放缓

  if (victoryCount <= softCap) {
    // 前 30 场：正常增长
    return 1 + (victoryCount * 0.15) + Math.pow(victoryCount, 2) * 0.003;
  } else {
    // 超过 30 场：增长放缓
    const baseAtCap = 1 + (softCap * 0.15) + Math.pow(softCap, 2) * 0.003;
    const beyond = victoryCount - softCap;
    return baseAtCap + (beyond * 0.05); // 每场只 +5%
  }
}

/**
 * 计算升级倍率（多项式温和增长）
 * @param {number} level - 等级
 * @returns {number} 倍率
 */
export function calculateLevelMultiplier(level) {
  return 1 + (level - 1) * 0.15 + Math.pow(level - 1, 2) * 0.005;
}

/**
 * 计算伤害
 * @param {object} attacker - 攻击方单位
 * @param {object} defender - 防御方单位
 * @param {boolean} isRanged - 是否远程攻击
 * @returns {object} 伤害结果
 */
export function calculateDamage(attacker, defender, isRanged = false) {
  // 1. 基础伤害
  let baseDamage = attacker.attack - (defender.defense || 0) * 0.5;

  // 2. 获取克制倍率
  const counterMod = getCounterModifier(attacker.id, defender.id);
  baseDamage *= counterMod.attackMultiplier;

  // 3. 暴击判定
  const baseCritChance = 0.1; // 10% 基础暴击
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

  return {
    damage: Math.floor(Math.max(1, baseDamage)),
    isCrit
  };
}

/**
 * 分析兵种克制关系
 * @param {array} playerUnits - 玩家单位数组
 * @param {array} enemyUnits - 敌方单位数组
 * @returns {object} 克制分析结果
 */
export function analyzeCounterBonus(playerUnits, enemyUnits) {
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

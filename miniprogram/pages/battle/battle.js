// pages/battle/battle.js
const app = getApp();
const { getUnitStats, getCounterModifier, analyzeCounterBonus } = require('../../utils/game-utils');

Page({
  data: {
    target: null,
    playerUnits: [],
    enemyUnits: [],
    round: 0,
    battleLog: [],
    logScrollId: '',
    battleEffect: {
      show: false,
      type: '',
      icon: '',
      text: ''
    },
    counterAdvantages: [],
    counterDisadvantages: [],
    difficultyScale: 100,
    battleInterval: null
  },

  onLoad() {
    const config = wx.getStorageSync('battleConfig');
    if (!config) {
      wx.navigateBack();
      return;
    }
    this.initBattle(config.target, config.playerUnits, config.scouted);
  },

  onUnload() {
    if (this.data.battleInterval) {
      clearInterval(this.data.battleInterval);
    }
  },

  initBattle(target, playerUnits, scouted) {
    // 生成敌方单位
    const enemyUnits = this.generateEnemyUnits(target.id);

    // 计算难度倍率
    const difficultyScale = Math.floor(this.calculateDifficultyScale() * 100);

    // 计算克制关系
    const counterAnalysis = analyzeCounterBonus(playerUnits, enemyUnits);

    this.setData({
      target: target,
      playerUnits: JSON.parse(JSON.stringify(playerUnits)),
      enemyUnits: enemyUnits,
      difficultyScale: difficultyScale,
      counterAdvantages: counterAnalysis.advantages,
      counterDisadvantages: counterAnalysis.disadvantages
    });

    // 添加战斗开始日志
    this.addLog('result', '⚔️', `战斗开始！${target.name}`);

    // 如果有侦察过，显示侦察信息
    if (scouted) {
      this.addLog('info', '🔍', '根据侦察情报，已了解敌方兵力配置');
    }

    // 显示克制提示
    if (counterAnalysis.advantages.length > 0) {
      this.addLog('player', '✅', `兵种克制：${counterAnalysis.advantages.join('、')}`);
    }
    if (counterAnalysis.disadvantages.length > 0) {
      this.addLog('enemy', '⚠️', `被克制：${counterAnalysis.disadvantages.join('、')}`);
    }

    // 开始自动战斗
    this.startAutoBattle();
  },

  // 生成敌方单位
  generateEnemyUnits(targetId) {
    const unitData = {
      infantry: { icon: '⚔️', name: '步兵' },
      archer: { icon: '🏹', name: '弓箭手' },
      pikeman: { icon: '🔱', name: '长矛兵' },
      shieldman: { icon: '🛡️', name: '盾兵' },
      cavalry: { icon: '🐴', name: '骑兵' },
      tank: { icon: '⚙️', name: '坦克' }
    };

    const configs = {
      1: [
        { id: 'infantry', count: 3 },
        { id: 'archer', count: 1 }
      ],
      2: [
        { id: 'infantry', count: 2 },
        { id: 'archer', count: 2 },
        { id: 'cavalry', count: 1 }
      ],
      3: [
        { id: 'infantry', count: 4 },
        { id: 'pikeman', count: 2 },
        { id: 'archer', count: 2 }
      ],
      4: [
        { id: 'infantry', count: 3 },
        { id: 'cavalry', count: 2 },
        { id: 'shieldman', count: 2 },
        { id: 'archer', count: 1 }
      ],
      5: [
        { id: 'infantry', count: 4 },
        { id: 'pikeman', count: 3 },
        { id: 'cavalry', count: 2 },
        { id: 'archer', count: 2 },
        { id: 'shieldman', count: 1 }
      ],
      6: [
        { id: 'cavalry', count: 4 },
        { id: 'archer', count: 3 },
        { id: 'infantry', count: 2 },
        { id: 'tank', count: 1 }
      ],
      7: [
        { id: 'infantry', count: 3 },
        { id: 'pikeman', count: 3 },
        { id: 'cavalry', count: 3 },
        { id: 'archer', count: 3 },
        { id: 'shieldman', count: 2 },
        { id: 'tank', count: 2 }
      ],
      8: [
        { id: 'infantry', count: 4 },
        { id: 'pikeman', count: 4 },
        { id: 'cavalry', count: 4 },
        { id: 'archer', count: 4 },
        { id: 'shieldman', count: 3 },
        { id: 'tank', count: 3 }
      ]
    };

    const config = configs[targetId] || configs[1];
    const units = [];
    let uid = 0;

    config.forEach(unit => {
      const stats = getUnitStats(unit.id, 1 + Math.floor(targetId / 2));
      for (let i = 0; i < unit.count; i++) {
        units.push({
          id: unit.id,
          icon: unitData[unit.id].icon,
          name: unitData[unit.id].name,
          uid: `${unit.id}_${uid++}`,
          hp: Math.floor(stats.hp * this.data.difficultyScale / 100),
          maxHp: Math.floor(stats.hp * this.data.difficultyScale / 100),
          attack: Math.floor(stats.attack * this.data.difficultyScale / 100)
        });
      }
    });

    return units;
  },

  // 计算难度倍率
  calculateDifficultyScale() {
    const victoryCount = app.globalData.gameData.victoryCount;
    const softCap = 30;

    if (victoryCount <= softCap) {
      return 1 + (victoryCount * 0.15) + Math.pow(victoryCount, 2) * 0.003;
    } else {
      const baseAtCap = 1 + (softCap * 0.15) + Math.pow(softCap, 2) * 0.003;
      const beyond = victoryCount - softCap;
      return baseAtCap + (beyond * 0.05);
    }
  },

  // 开始自动战斗
  startAutoBattle() {
    let round = 0;

    this.setData({
      battleInterval: setInterval(() => {
        round++;
        this.executeRound(round);
      }, 1200)
    });
  },

  // 执行回合
  executeRound(round) {
    const { playerUnits, enemyUnits } = this.data;

    // 检查是否结束
    const playerAlive = playerUnits.filter(u => u.hp > 0);
    const enemyAlive = enemyUnits.filter(u => u.hp > 0);

    if (playerAlive.length === 0) {
      this.endBattle(false);
      return;
    }

    if (enemyAlive.length === 0) {
      this.endBattle(true);
      return;
    }

    this.setData({ round });

    // 玩家攻击
    const attacker = playerAlive[Math.floor(Math.random() * playerAlive.length)];
    const defender = enemyAlive[Math.floor(Math.random() * enemyAlive.length)];

    // 计算克制倍率
    const counterMod = getCounterModifier(attacker.id, defender.id);

    // 计算伤害
    let damage = Math.max(1, Math.floor(attacker.attack * counterMod.attackMultiplier));

    // 暴击判定
    const critChance = 0.1 + Math.max(0, counterMod.critBonus || 0);
    const isCrit = Math.random() < critChance;
    if (isCrit) {
      damage = Math.floor(damage * 1.5);
    }

    // 更新敌方 HP
    const enemyIndex = enemyUnits.findIndex(u => u.uid === defender.uid);
    if (enemyIndex !== -1) {
      enemyUnits[enemyIndex].hp = Math.max(0, enemyUnits[enemyIndex].hp - damage);
    }

    // 显示攻击动画
    this.showBattleEffect('player', isCrit ? 'crit' : 'normal', attacker.icon, `-${damage}`);

    // 添加日志
    const logIcon = isCrit ? '💥' : '⚔️';
    this.addLog(isCrit ? 'crit' : 'player', logIcon, `${attacker.icon}${attacker.name} 攻击 ${defender.icon} 造成 ${damage} ${isCrit ? '(暴击!)' : ''} 伤害`);

    // 检查敌人是否死亡
    if (enemyUnits[enemyIndex].hp <= 0) {
      setTimeout(() => {
        this.addLog('result', '💀', `敌方 ${defender.icon}${defender.name} 被击败`);
      }, 300);
    }

    this.setData({ enemyUnits });

    // 敌人反击（延迟）
    setTimeout(() => {
      const currentEnemyAlive = this.data.enemyUnits.filter(u => u.hp > 0);
      const currentPlayerAlive = this.data.playerUnits.filter(u => u.hp > 0);

      if (currentEnemyAlive.length > 0 && currentPlayerAlive.length > 0) {
        const enemyAttacker = currentEnemyAlive[Math.floor(Math.random() * currentEnemyAlive.length)];
        const playerDefender = currentPlayerAlive[Math.floor(Math.random() * currentPlayerAlive.length)];

        const enemyCounterMod = getCounterModifier(enemyAttacker.id, playerDefender.id);
        let enemyDamage = Math.max(1, Math.floor(enemyAttacker.attack * enemyCounterMod.attackMultiplier));

        const enemyCritChance = 0.1 + Math.max(0, enemyCounterMod.critBonus || 0);
        const isEnemyCrit = Math.random() < enemyCritChance;
        if (isEnemyCrit) {
          enemyDamage = Math.floor(enemyDamage * 1.5);
        }

        // 更新玩家 HP
        const playerIndex = this.data.playerUnits.findIndex(u => u.uid === playerDefender.uid);
        if (playerIndex !== -1) {
          this.data.playerUnits[playerIndex].hp = Math.max(0, this.data.playerUnits[playerIndex].hp - enemyDamage);
        }

        // 显示攻击动画
        this.showBattleEffect('enemy', isEnemyCrit ? 'crit' : 'normal', enemyAttacker.icon, `-${enemyDamage}`);

        // 添加日志
        const logIcon = isEnemyCrit ? '💥' : '⚔️';
        this.addLog(isEnemyCrit ? 'crit' : 'enemy', logIcon, `敌方${enemyAttacker.icon} 攻击 ${playerDefender.icon} 造成 ${enemyDamage} ${isEnemyCrit ? '(暴击!)' : ''} 伤害`);

        if (this.data.playerUnits[playerIndex].hp <= 0) {
          this.addLog('result', '💀', `我方 ${playerDefender.icon}${playerDefender.name} 被击败`);
        }

        this.setData({ playerUnits: this.data.playerUnits });
      }
    }, 600);
  },

  // 显示战斗效果
  showBattleEffect(side, type, icon, text) {
    this.setData({
      'battleEffect.show': true,
      'battleEffect.type': side,
      'battleEffect.icon': icon,
      'battleEffect.text': text
    });

    setTimeout(() => {
      this.setData({
        'battleEffect.show': false
      });
    }, 500);
  },

  // 添加日志
  addLog(type, icon, text) {
    const logs = this.data.battleLog;
    const id = Date.now() + Math.random();
    logs.push({ id, type, icon, text });
    this.setData({
      battleLog: logs,
      logScrollId: `log-${logs.length - 1}`
    });
  },

  // 跳过战斗
  skipBattle() {
    const playerPower = this.data.playerUnits.filter(u => u.hp > 0).reduce((sum, u) => sum + u.attack, 0);
    const enemyPower = this.data.enemyUnits.filter(u => u.hp > 0).reduce((sum, u) => sum + u.attack, 0);

    const isWin = playerPower > enemyPower;
    this.endBattle(isWin);
  },

  // 结束战斗
  endBattle(isVictory) {
    if (this.data.battleInterval) {
      clearInterval(this.data.battleInterval);
    }

    const gameData = app.globalData.gameData;
    gameData.stats.totalBattles++;

    if (isVictory) {
      // 胜利
      const reward = Math.floor(this.data.target.reward * this.data.difficultyScale);
      gameData.gold += reward;
      gameData.victoryCount++;
      gameData.stats.totalWins++;
      gameData.consecutiveLosses = 0;

      if (!gameData.conqueredTerritories.includes(this.data.target.id)) {
        gameData.conqueredTerritories.push(this.data.target.id);
      }

      // 检查是否通关
      if (gameData.conqueredTerritories.length >= 8) {
        gameData.gameVictory = true;
      }

      this.addLog('result', '🎉', `胜利！获得 ${reward} 金币`);

      setTimeout(() => {
        app.saveGameData();
        wx.navigateTo({
          url: `/pages/result/result?victory=true&reward=${reward}`
        });
      }, 1500);
    } else {
      // 失败
      gameData.stats.totalLosses++;
      gameData.consecutiveLosses++;

      this.addLog('result', '💀', `失败！军团全军覆没`);

      // 检查 Game Over
      if (gameData.consecutiveLosses >= 3) {
        gameData.gameOver = true;
        gameData.gameOverReason = 'consecutive_defeats';
      }

      setTimeout(() => {
        app.saveGameData();
        wx.navigateTo({
          url: `/pages/result/result?victory=false`
        });
      }, 1500);
    }
  }
});

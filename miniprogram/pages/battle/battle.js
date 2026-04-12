// pages/battle/battle.js
const app = getApp();

Page({
  data: {
    target: null,
    playerUnits: [],
    enemyUnits: [],
    round: 0,
    battleLog: [],
    lastAction: null,
    battleInterval: null
  },

  onLoad() {
    // 加载战斗配置
    const config = wx.getStorageSync('battleConfig');
    if (!config) {
      wx.navigateBack();
      return;
    }

    this.initBattle(config.target, config.playerUnits);
  },

  onUnload() {
    if (this.data.battleInterval) {
      clearInterval(this.data.battleInterval);
    }
  },

  initBattle(target, playerUnits) {
    // 生成敌方单位
    const enemyUnits = this.generateEnemyUnits(target);

    this.setData({
      target: target,
      playerUnits: JSON.parse(JSON.stringify(playerUnits)),
      enemyUnits: enemyUnits
    });

    // 添加战斗开始日志
    this.addLog('result', `⚔️ 战斗开始！${target.name}`);

    // 开始自动战斗
    this.startAutoBattle();
  },

  generateEnemyUnits(target) {
    // 根据关卡生成敌军
    const enemyConfig = {
      1: [
        { id: 'infantry', icon: '⚔️', count: 3, hp: 100, maxHp: 100, attack: 20 },
        { id: 'archer', icon: '🏹', count: 1, hp: 80, maxHp: 80, attack: 30 }
      ],
      2: [
        { id: 'infantry', icon: '⚔️', count: 2, hp: 100, maxHp: 100, attack: 20 },
        { id: 'archer', icon: '🏹', count: 2, hp: 80, maxHp: 80, attack: 30 },
        { id: 'cavalry', icon: '🐴', count: 1, hp: 100, maxHp: 100, attack: 42 }
      ]
    };

    const config = enemyConfig[target.id] || enemyConfig[1];
    const units = [];
    config.forEach((unit, index) => {
      for (let i = 0; i < unit.count; i++) {
        units.push({
          ...unit,
          uid: `${unit.id}_${index}_${i}`
        });
      }
    });

    return units;
  },

  startAutoBattle() {
    let round = 0;

    this.setData({
      battleInterval: setInterval(() => {
        round++;
        this.executeRound(round);
      }, 1000)
    });
  },

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

    // 玩家攻击
    const attacker = playerAlive[Math.floor(Math.random() * playerAlive.length)];
    const defender = enemyAlive[Math.floor(Math.random() * enemyAlive.length)];

    const damage = Math.max(1, attacker.attack);
    defender.hp = Math.max(0, defender.hp - damage);

    this.setData({
      [`enemyUnits[${enemyUnits.findIndex(u => u.uid === defender.uid)}]`]: defender,
      lastAction: {
        isPlayer: true,
        text: `${attacker.icon} 造成 ${damage} 点伤害`
      }
    });

    this.addLog('player', `${attacker.icon}${attacker.name} 攻击 ${defender.icon} 造成 ${damage} 伤害`);

    // 检查敌人是否死亡
    if (defender.hp <= 0) {
      this.addLog('result', `💀 敌方 ${defender.icon} 被击败`);
    }

    // 敌人反击（下一回合）
    setTimeout(() => {
      if (enemyAlive.length > 0 && playerAlive.length > 0) {
        const enemyAttacker = enemyAlive[Math.floor(Math.random() * enemyAlive.length)];
        const playerDefender = playerAlive[Math.floor(Math.random() * playerAlive.length)];

        const enemyDamage = Math.max(1, enemyAttacker.attack);
        playerDefender.hp = Math.max(0, playerDefender.hp - enemyDamage);

        this.setData({
          [`playerUnits[${playerUnits.findIndex(u => u.uid === playerDefender.uid)}]`]: playerDefender,
          lastAction: {
            isPlayer: false,
            text: `敌方造成 ${enemyDamage} 点伤害`
          }
        });

        this.addLog('enemy', `敌方${enemyAttacker.icon} 攻击 ${playerDefender.icon} 造成 ${enemyDamage} 伤害`);

        if (playerDefender.hp <= 0) {
          this.addLog('result', `💀 我方 ${playerDefender.icon} 被击败`);
        }
      }
    }, 500);

    this.setData({ round });
  },

  addLog(type, text) {
    const logs = this.data.battleLog;
    logs.push({ id: Date.now(), type, text });
    this.setData({ battleLog: logs });
  },

  skipBattle() {
    // 快速计算结果
    const playerPower = this.data.playerUnits.reduce((sum, u) => sum + u.attack, 0);
    const enemyPower = this.data.enemyUnits.reduce((sum, u) => sum + u.attack, 0);

    const isWin = playerPower > enemyPower;
    this.endBattle(isWin);
  },

  endBattle(isVictory) {
    if (this.data.battleInterval) {
      clearInterval(this.data.battleInterval);
    }

    const gameData = app.globalData.gameData;

    if (isVictory) {
      // 胜利
      gameData.gold += this.data.target.reward;
      gameData.victoryCount++;
      gameData.stats.totalWins++;
      gameData.consecutiveLosses = 0;

      if (!gameData.conqueredTerritories.includes(this.data.target.id)) {
        gameData.conqueredTerritories.push(this.data.target.id);
      }

      this.addLog('result', `🎉 胜利！获得 ${this.data.target.reward} 金币`);

      setTimeout(() => {
        app.saveGameData();
        wx.navigateTo({
          url: `/pages/result/result?victory=true&reward=${this.data.target.reward}`
        });
      }, 1500);
    } else {
      // 失败
      gameData.stats.totalLosses++;
      gameData.consecutiveLosses++;

      this.addLog('result', `💀 失败！军团全军覆没`);

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

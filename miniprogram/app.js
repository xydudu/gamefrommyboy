// app.js
App({
  onLaunch() {
    // 初始化游戏数据
    this.initGameData();
  },

 .globalData: {
    // 游戏数据
    gameData: null,

    // 兵种配置
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
        baseAttack: 30,
        baseHp: 80,
        desc: '远程攻击单位，高攻低防'
      },
      {
        id: 'pikeman',
        name: '长矛兵',
        icon: '🔱',
        unlocked: false,
        unlockCost: 300,
        baseCost: 100,
        baseAttack: 22,
        baseHp: 140,
        desc: '反骑兵专家，高血量'
      },
      {
        id: 'shieldman',
        name: '盾兵',
        icon: '🛡️',
        unlocked: false,
        unlockCost: 400,
        baseCost: 120,
        baseAttack: 18,
        baseHp: 180,
        desc: '防御型单位，极高血量'
      },
      {
        id: 'cavalry',
        name: '骑兵',
        icon: '🐴',
        unlocked: false,
        unlockCost: 500,
        baseCost: 150,
        baseAttack: 42,
        baseHp: 100,
        desc: '高速突击单位，克制弓箭手'
      },
      {
        id: 'tank',
        name: '坦克',
        icon: '⚙️',
        unlocked: false,
        unlockCost: 600,
        baseCost: 200,
        baseAttack: 55,
        baseHp: 220,
        desc: '终极战争机器，攻守兼备'
      }
    ],

    // 关卡配置
    targets: [
      { id: 1, name: '边境哨站', difficulty: 'easy', attack: 50, defense: 30, reward: 200 },
      { id: 2, name: '强盗营地', difficulty: 'easy', attack: 80, defense: 50, reward: 350 },
      { id: 3, name: '废弃城堡', difficulty: 'medium', attack: 120, defense: 80, reward: 500 },
      { id: 4, name: '兽人部落', difficulty: 'medium', attack: 150, defense: 100, reward: 700 },
      { id: 5, name: '黑暗要塞', difficulty: 'hard', attack: 200, defense: 150, reward: 1000 },
      { id: 6, name: '龙之巢穴', difficulty: 'hard', attack: 300, defense: 200, reward: 1500 },
      { id: 7, name: '恶魔王座', difficulty: 'hard', attack: 400, defense: 300, reward: 2000 },
      { id: 8, name: '虚空神殿', difficulty: 'hard', attack: 500, defense: 400, reward: 3000 }
    ],

    // 兵种克制配置
    unitCounters: {
      infantry: { strong: ['cavalry'], weak: ['archer'] },
      archer: { strong: ['infantry'], weak: ['cavalry'] },
      cavalry: { strong: ['archer'], weak: ['infantry'] },
      pikeman: { strong: ['cavalry'], weak: ['archer'], bonusVs: ['cavalry'] },
      shieldman: { strong: ['infantry'], weak: ['cavalry'], resistVs: ['archer'] },
      tank: { strong: [], weak: [], immune: true }
    }
  },

  initGameData() {
    this.globalData.gameData = {
      gold: 1000,
      recruitedUnits: [],
      conqueredTerritories: [],
      scoutedTerritories: [],
      victoryCount: 0,
      consecutiveLosses: 0,
      gameOver: false,
      gameVictory: false,
      unitLevels: {},
      stats: {
        totalBattles: 0,
        totalWins: 0,
        totalLosses: 0,
        startTime: Date.now()
      }
    };

    // 初始化兵种等级
    this.globalData.units.forEach(unit => {
      this.globalData.gameData.unitLevels[unit.id] = {
        level: 1,
        upgradeCost: Math.floor(unit.baseCost * 0.8),
        unlocked: unit.unlocked
      };
    });
  },

  // 保存到本地存储
  saveGameData() {
    wx.setStorageSync('gameData', this.globalData.gameData);
  },

  // 从本地存储加载
  loadGameData() {
    const data = wx.getStorageSync('gameData');
    if (data) {
      this.globalData.gameData = data;
      return true;
    }
    return false;
  }
});

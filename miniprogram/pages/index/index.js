// pages/index/index.js
const app = getApp();

Page({
  data: {
    gold: 1000,
    victoryCount: 0,
    consecutiveLosses: 0,
    recruitedUnits: [],
    targets: [],
    availableUnits: [],
    selectedTarget: null,
    inBattle: false,
    toast: {
      show: false,
      icon: 'ℹ️',
      title: '',
      message: ''
    }
  },

  onLoad() {
    this.initGame();
  },

  onShow() {
    // 每次显示时刷新数据
    this.refreshUI();
  },

  initGame() {
    // 尝试加载存档
    const hasSave = app.loadGameData();
    if (!hasSave) {
      app.initGameData();
    }
    this.refreshUI();
  },

  refreshUI() {
    const gameData = app.globalData.gameData;
    this.setData({
      gold: gameData.gold,
      victoryCount: gameData.victoryCount,
      consecutiveLosses: gameData.consecutiveLosses,
      recruitedUnits: gameData.recruitedUnits,
      targets: app.globalData.targets,
      availableUnits: app.globalData.units,
      gameData: gameData
    });
  },

  // 检查领地是否已征服
  isConquered(id) {
    return this.data.recruitedUnits.some(t => t.id === id);
  },

  // 获取难度文本
  getDifficultyText(difficulty) {
    const map = {
      easy: '简单',
      medium: '中等',
      hard: '困难'
    };
    return map[difficulty] || difficulty;
  },

  // 选择目标
  selectTarget(e) {
    const id = e.currentTarget.dataset.id;
    const target = app.globalData.targets.find(t => t.id === id);

    if (this.data.selectedTarget === id) {
      this.setData({ selectedTarget: null });
    } else {
      this.setData({ selectedTarget: id });
      this.showToast('info', '已选择', `目标：${target.name}`);
    }
  },

  // 招募兵种
  recruitUnit(e) {
    const unit = e.currentTarget.dataset.unit;
    const gameData = app.globalData.gameData;
    const unitLevel = gameData.unitLevels[unit.id];

    // 检查是否已解锁
    if (!unitLevel.unlocked) {
      this.showToast('error', '未解锁', `需要 ${unit.unlockCost} 金币解锁`);
      return;
    }

    // 检查金币
    if (gameData.gold < unit.baseCost) {
      this.showToast('error', '金币不足', `需要 ${unit.baseCost} 金币`);
      return;
    }

    // 招募
    gameData.gold -= unit.baseCost;
    gameData.recruitedUnits.push({
      id: unit.id,
      name: unit.name,
      icon: unit.icon,
      hp: unit.baseHp,
      maxHp: unit.baseHp,
      attack: unit.baseAttack
    });

    app.saveGameData();
    this.refreshUI();
    this.showToast('success', '招募成功', `${unit.name} 加入军团`);
  },

  // 开始战斗
  startBattle() {
    if (!this.data.selectedTarget) {
      this.showToast('warning', '请选择目标', '先选择一个征战的领地');
      return;
    }

    if (this.data.recruitedUnits.length === 0) {
      this.showToast('warning', '没有兵力', '请先招募兵种');
      return;
    }

    const target = app.globalData.targets.find(t => t.id === this.data.selectedTarget);

    // 保存战斗数据
    wx.setStorageSync('battleConfig', {
      target: target,
      playerUnits: JSON.parse(JSON.stringify(this.data.recruitedUnits))
    });

    // 跳转到战斗页面
    wx.navigateTo({
      url: '/pages/battle/battle'
    });
  },

  // 返回地图
  returnToMap() {
    this.setData({ inBattle: false });
  },

  // Toast 提示
  showToast(type, title, message, duration = 2000) {
    const icons = {
      info: 'ℹ️',
      warning: '⚠️',
      error: '❌',
      success: '✅'
    };

    this.setData({
      toast: {
        show: true,
        icon: icons[type] || icons.info,
        title: title,
        message: message
      }
    });

    setTimeout(() => {
      this.setData({
        'toast.show': false
      });
    }, duration);
  }
});

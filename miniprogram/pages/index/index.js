// pages/index/index.js
const app = getApp();
const { getUnitStats, calculateUpgradeCost } = require('../../utils/game-utils');

Page({
  data: {
    gold: 1000,
    victoryCount: 0,
    consecutiveLosses: 0,
    recruitedUnits: [],
    targets: [],
    availableUnits: [],
    upgradeableUnits: [],
    selectedTarget: null,
    inBattle: false,
    showArmyPanel: false,
    showScoutModal: false,
    showUpgradeModal: false,
    healCost: 0,
    scoutData: {
      targetName: '',
      enemies: []
    },
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
    this.refreshUI();
    this.checkWarnings();
  },

  initGame() {
    const hasSave = app.loadGameData();
    if (!hasSave) {
      app.initGameData();
    }
    this.refreshUI();
  },

  refreshUI() {
    const gameData = app.globalData.gameData;
    const units = app.globalData.units;

    // 计算治疗费用
    const woundedUnits = gameData.recruitedUnits.filter(u => u.hp < u.maxHp);
    const healCost = woundedUnits.length * 20;

    this.setData({
      gold: gameData.gold,
      victoryCount: gameData.victoryCount,
      consecutiveLosses: gameData.consecutiveLosses,
      recruitedUnits: gameData.recruitedUnits,
      targets: app.globalData.targets,
      availableUnits: units,
      upgradeableUnits: units,
      gameData: gameData,
      healCost: healCost
    });
  },

  // 检查警告
  checkWarnings() {
    const { consecutiveLosses, gold } = this.data;

    if (consecutiveLosses >= 1) {
      const text = consecutiveLosses === 1 ? '军心不稳' : '濒临崩溃';
      this.showToast('warning', text, `已连败${consecutiveLosses}场`);
    }

    if (gold < 50 && consecutiveLosses === 0) {
      this.showToast('warning', '财政紧张', '金币不足，请速征战补给');
    }
  },

  // 切换军团面板
  toggleArmyPanel() {
    this.setData({
      showArmyPanel: !this.data.showArmyPanel
    });
  },

  // 切换升级弹窗
  toggleUpgradeModal() {
    this.setData({
      showUpgradeModal: !this.data.showUpgradeModal
    });
  },

  // 关闭侦察弹窗
  closeScoutModal() {
    this.setData({ showScoutModal: false });
  },

  // 关闭升级弹窗
  closeUpgradeModal() {
    this.setData({ showUpgradeModal: false });
  },

  // 阻止事件冒泡
  stopPropagation(e) {
    e.stopPropagation();
  },

  // 检查领地是否已征服
  isConquered(id) {
    return app.globalData.gameData.conqueredTerritories.includes(id);
  },

  // 获取难度文本
  getDifficultyText(difficulty) {
    const map = { easy: '简单', medium: '中等', hard: '困难' };
    return map[difficulty] || difficulty;
  },

  // 获取兵种攻击
  getUnitAttack(unitId) {
    const stats = getUnitStats(unitId, this.data.gameData.unitLevels[unitId].level);
    return stats.attack;
  },

  // 获取兵种 HP
  getUnitHp(unitId) {
    const stats = getUnitStats(unitId, this.data.gameData.unitLevels[unitId].level);
    return stats.hp;
  },

  // 获取升级费用
  getUpgradeCost(unitId) {
    return this.data.gameData.unitLevels[unitId].upgradeCost;
  },

  // 选择目标
  selectTarget(e) {
    const id = e.currentTarget.dataset.id;
    const target = app.globalData.targets.find(t => t.id === id);

    if (this.data.selectedTarget === id) {
      this.setData({ selectedTarget: null });
      this.showToast('info', '取消选择', `不再征战${target.name}`);
    } else {
      this.setData({ selectedTarget: id });
      this.showToast('success', '已选择', `目标：${target.name}`);
    }
  },

  // 侦察目标
  scoutTarget(e) {
    e.stopPropagation();
    const id = e.currentTarget.dataset.id;
    this.scoutEnemy(id);
  },

  // 侦察功能
  scoutEnemy(id) {
    const gameData = app.globalData.gameData;
    const target = app.globalData.targets.find(t => t.id === id);

    // 检查是否已侦察过
    if (gameData.scoutedTerritories?.includes(id)) {
      this.showScoutResult(target.id);
      return;
    }

    const scoutCost = 100;

    // 检查金币
    if (gameData.gold < scoutCost) {
      this.showToast('error', '金币不足', `侦察需要 ${scoutCost} 金币`);
      return;
    }

    // 扣除金币
    gameData.gold -= scoutCost;

    // 标记为已侦察
    if (!gameData.scoutedTerritories) {
      gameData.scoutedTerritories = [];
    }
    gameData.scoutedTerritories.push(id);

    app.saveGameData();
    this.refreshUI();
    this.showScoutResult(id);
  },

  // 显示侦察结果
  showScoutResult(targetId) {
    const target = app.globalData.targets.find(t => t.id === targetId);

    // 生成敌军情报
    const enemyConfig = this.getEnemyConfig(targetId);
    const enemies = enemyConfig.map(unit => ({
      icon: unit.icon,
      name: unit.name,
      count: unit.count,
      id: unit.id
    }));

    this.setData({
      'scoutData.targetName': target.name,
      'scoutData.enemies': enemies,
      showScoutModal: true
    });
  },

  // 获取敌军配置
  getEnemyConfig(targetId) {
    const configs = {
      1: [
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 3 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 1 }
      ],
      2: [
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 2 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 2 },
        { id: 'cavalry', icon: '🐴', name: '骑兵', count: 1 }
      ],
      3: [
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 4 },
        { id: 'pikeman', icon: '🔱', name: '长矛兵', count: 2 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 2 }
      ],
      4: [
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 3 },
        { id: 'cavalry', icon: '🐴', name: '骑兵', count: 2 },
        { id: 'shieldman', icon: '🛡️', name: '盾兵', count: 2 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 1 }
      ],
      5: [
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 4 },
        { id: 'pikeman', icon: '🔱', name: '长矛兵', count: 3 },
        { id: 'cavalry', icon: '🐴', name: '骑兵', count: 2 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 2 },
        { id: 'shieldman', icon: '🛡️', name: '盾兵', count: 1 }
      ],
      6: [
        { id: 'cavalry', icon: '🐴', name: '骑兵', count: 4 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 3 },
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 2 },
        { id: 'tank', icon: '⚙️', name: '坦克', count: 1 }
      ],
      7: [
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 3 },
        { id: 'pikeman', icon: '🔱', name: '长矛兵', count: 3 },
        { id: 'cavalry', icon: '🐴', name: '骑兵', count: 3 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 3 },
        { id: 'shieldman', icon: '🛡️', name: '盾兵', count: 2 },
        { id: 'tank', icon: '⚙️', name: '坦克', count: 2 }
      ],
      8: [
        { id: 'infantry', icon: '⚔️', name: '步兵', count: 4 },
        { id: 'pikeman', icon: '🔱', name: '长矛兵', count: 4 },
        { id: 'cavalry', icon: '🐴', name: '骑兵', count: 4 },
        { id: 'archer', icon: '🏹', name: '弓箭手', count: 4 },
        { id: 'shieldman', icon: '🛡️', name: '盾兵', count: 3 },
        { id: 'tank', icon: '⚙️', name: '坦克', count: 3 }
      ]
    };
    return configs[targetId] || configs[1];
  },

  // 处理兵种点击（招募或解锁）
  handleUnitTap(e) {
    const unit = e.currentTarget.dataset.unit;
    const gameData = app.globalData.gameData;
    const unitLevel = gameData.unitLevels[unit.id];

    if (unitLevel.unlocked) {
      // 已解锁，招募
      this.recruitUnit(unit);
    } else {
      // 未解锁，解锁
      this.unlockUnit(unit);
    }
  },

  // 解锁兵种
  unlockUnit(unit) {
    const gameData = app.globalData.gameData;

    if (gameData.gold >= unit.unlockCost) {
      gameData.gold -= unit.unlockCost;
      gameData.unitLevels[unit.id].unlocked = true;
      app.saveGameData();
      this.refreshUI();
      this.showToast('success', '解锁成功', `${unit.name} 已解锁，可以招募了！`);
    } else {
      this.showToast('error', '金币不足', `需要 ${unit.unlockCost} 金币解锁`);
    }
  },

  // 招募兵种
  recruitUnit(unit) {
    const gameData = app.globalData.gameData;

    if (gameData.gold >= unit.baseCost) {
      gameData.gold -= unit.baseCost;
      const stats = getUnitStats(unit.id, gameData.unitLevels[unit.id].level);
      gameData.recruitedUnits.push({
        id: unit.id,
        name: unit.name,
        icon: unit.icon,
        hp: stats.hp,
        maxHp: stats.hp,
        attack: stats.attack,
        uid: Date.now() + Math.random()
      });
      app.saveGameData();
      this.refreshUI();
      this.showToast('success', '招募成功', `${unit.name} 加入军团`);
    } else {
      this.showToast('error', '金币不足', `需要 ${unit.baseCost} 金币`);
    }
  },

  // 升级兵种
  upgradeUnit(e) {
    const unit = e.currentTarget.dataset.unit;
    const gameData = app.globalData.gameData;
    const unitLevel = gameData.unitLevels[unit.id];
    const upgradeCost = unitLevel.upgradeCost;

    if (!unitLevel.unlocked) {
      this.showToast('error', '未解锁', `先解锁该兵种`);
      return;
    }

    if (gameData.gold >= upgradeCost) {
      gameData.gold -= upgradeCost;
      unitLevel.level++;
      unitLevel.upgradeCost = Math.floor(upgradeCost * 1.5);
      app.saveGameData();
      this.refreshUI();
      this.showToast('success', '升级成功', `${unit.name} 提升至 Lv.${unitLevel.level}`);
    } else {
      this.showToast('error', '金币不足', `升级需要 ${upgradeCost} 金币`);
    }
  },

  // 治疗单个单位
  healUnit(e) {
    const index = e.currentTarget.dataset.index;
    const unit = this.data.recruitedUnits[index];
    const gameData = app.globalData.gameData;

    if (unit.hp >= unit.maxHp) {
      this.showToast('info', '已满血', `${unit.name} 生命值已满`);
      return;
    }

    const healCost = 20;
    if (gameData.gold >= healCost) {
      gameData.gold -= healCost;
      unit.hp = unit.maxHp;
      app.saveGameData();
      this.refreshUI();
      this.showToast('success', '治疗成功', `${unit.name} 已恢复满生命值`);
    } else {
      this.showToast('error', '金币不足', `治疗需要 ${healCost} 金币`);
    }
  },

  // 解散单位
  dismissUnit(e) {
    const index = e.currentTarget.dataset.index;
    const gameData = app.globalData.gameData;

    gameData.recruitedUnits.splice(index, 1);
    app.saveGameData();
    this.refreshUI();
    this.showToast('info', '已解散', '单位已解散');
  },

  // 全体治疗
  healAllUnits() {
    const gameData = app.globalData.gameData;
    const woundedUnits = gameData.recruitedUnits.filter(u => u.hp < u.maxHp);
    const healCost = woundedUnits.length * 20;

    if (woundedUnits.length === 0) {
      this.showToast('info', '无需治疗', '所有单位都已满血');
      return;
    }

    if (gameData.gold >= healCost) {
      gameData.gold -= healCost;
      gameData.recruitedUnits.forEach(u => u.hp = u.maxHp);
      app.saveGameData();
      this.refreshUI();
      this.showToast('success', '治疗成功', `已恢复${woundedUnits.length}个单位`);
    } else {
      this.showToast('error', '金币不足', `全体治疗需要 ${healCost} 金币`);
    }
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
      playerUnits: JSON.parse(JSON.stringify(this.data.recruitedUnits)),
      scouted: app.globalData.gameData.scoutedTerritories?.includes(target.id)
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

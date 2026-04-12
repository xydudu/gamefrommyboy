// pages/result/result.js
const app = getApp();

Page({
  data: {
    victory: false,
    reward: 0,
    victoryCount: 0,
    consecutiveLosses: 0,
    conqueredTerritories: 0,
    totalBattles: 0,
    totalLosses: 0,
    gold: 0,
    gameOver: false,
    gameOverReason: '',
    gameVictory: false,
    playTime: 0
  },

  onLoad(options) {
    const gameData = app.globalData.gameData;

    // 计算游戏时间
    const playTime = Math.floor((Date.now() - gameData.stats.startTime) / 60000);

    this.setData({
      victory: options.victory === 'true',
      reward: options.reward || 0,
      victoryCount: gameData.victoryCount,
      consecutiveLosses: gameData.consecutiveLosses,
      conqueredTerritories: gameData.conqueredTerritories.length,
      totalBattles: gameData.stats.totalBattles,
      totalLosses: gameData.stats.totalLosses,
      gold: gameData.gold,
      gameOver: gameData.gameOver,
      gameOverReason: this.getGameOverReason(gameData.gameOverReason),
      gameVictory: gameData.gameVictory,
      playTime: playTime
    });

    // 如果游戏结束或通关，显示对应弹窗
    if (gameData.gameOver || gameData.gameVictory) {
      // 不需要额外操作，wxml 会自动显示弹窗
    }
  },

  getGameOverReason(reason) {
    const map = {
      consecutive_defeats: '连战连败，军心溃散',
      no_resources_no_land: '资源耗尽，穷途末路',
      surrender: '主动投降，虽败犹荣'
    };
    return map[reason] || '军团覆灭';
  },

  continueGame() {
    if (this.data.gameOver || this.data.gameVictory) {
      return;
    }
    wx.navigateBack();
  },

  restartGame() {
    wx.showModal({
      title: '重新开始',
      content: '确定要重新开始游戏吗？当前进度将会丢失！',
      confirmText: '重新开始',
      confirmColor: '#ff2d55',
      success: (res) => {
        if (res.confirm) {
          app.initGameData();
          app.saveGameData();
          wx.redirectTo({
            url: '/pages/index/index'
          });
        }
      }
    });
  }
});

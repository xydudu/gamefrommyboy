// pages/result/result.js
const app = getApp();

Page({
  data: {
    victory: false,
    reward: 0,
    victoryCount: 0,
    consecutiveLosses: 0,
    gameOver: false,
    gameOverReason: ''
  },

  onLoad(options) {
    const gameData = app.globalData.gameData;

    this.setData({
      victory: options.victory === 'true',
      reward: options.reward || 0,
      victoryCount: gameData.victoryCount,
      consecutiveLosses: gameData.consecutiveLosses,
      gameOver: gameData.gameOver,
      gameOverReason: this.getGameOverReason(gameData.gameOverReason)
    });
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
    if (this.data.gameOver) {
      return;
    }
    wx.navigateBack();
  },

  restartGame() {
    app.initGameData();
    app.saveGameData();
    wx.redirectTo({
      url: '/pages/index/index'
    });
  }
});

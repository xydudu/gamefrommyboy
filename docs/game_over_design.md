# Game Over 机制设计文档

**版本**: v1.3 (已实现)  
**日期**: 2026-04-12  
**最后更新**: 2026-04-12 (连败淘汰制实现)  
**使用工具**: game-designer-toolkit

---

## 一、问题分析

### 当前设计的缺陷

1. **招募时金币不足 → Game Over** ❌
   - 玩家还未开始战斗，只是经济管理失误
   - 剥夺了玩家翻盘的机会
   - 挫败感过强，不符合游戏节奏

2. **金币 < 50 就判定破产** ❌
   - 没有考虑玩家可能故意存钱爆发
   - 忽略了征战是主要收入来源

### 正确的 Game Over 设计原则

根据 game-designer-toolkit 框架：

| 原则 | 说明 |
|------|------|
| **失败来自决策** | 玩家做出错误选择后承担后果 |
| **有预警时间** | 提前警告，给玩家反应机会 |
| **有翻盘可能** | 除非玩家主动放弃，否则有希望 |
| **清晰透明** | 玩家知道为什么失败 |

---

## 二、优化方案

### 方案 A：连败淘汰制（推荐）

```
Game Over 条件：
1. 连续失败 3 场 → Game Over
2. 主动投降 → Game Over
3. 金币 < 20 且无未征服领地 → Game Over（穷途末路）
```

**设计原理**：
- 连败说明玩家策略有问题，给 3 次机会合理
- 单场失败不结束，给玩家调整机会
- 金币不足时，如果还有领地可打，就有翻盘希望

### 方案 B：领地全失制

```
Game Over 条件：
1. 所有已征服领地全部丢失 → Game Over
2. 连续失败 5 场 → Game Over
```

**设计原理**：
- 类似策略游戏的"首都沦陷"概念
- 给玩家更大的容错空间

### 方案 C：综合判定（最终采用）

```
Game Over 触发条件：

【硬性条件】
1. 连续失败 ≥ 3 场
2. 主动返回地图时金币 < 30 且已无未征服领地

【软性条件】
3. 征战中全军覆没（所有兵种 HP ≤ 0）→ 本场失败，计入连败

【不触发 Game Over 的情况】
- 招募时金币不足 → 仅提示
- 升级时金币不足 → 仅提示
- 侦察时金币不足 → 仅提示
- 单场战斗失败 → 计入连败，但不结束
```

---

## 三、预警系统

### 三级预警机制

| 级别 | 触发条件 | 提示内容 | 类型 |
|------|----------|----------|------|
| **黄色** | 连败 1 场 | 军心不稳，下一战需谨慎 | Toast |
| **橙色** | 连败 2 场 | 再失败一次，军团将溃散！ | Toast + 震动 |
| **红色** | 金币 < 50 | 财政危机，请速征战补给 | Toast |

### 预警 UI 设计

```html
<!-- 连败指示器 -->
<div class="defeat-streak-indicator" data-streak="2">
    <span class="streak-icon">💀</span>
    <span class="streak-count">2</span>
    <span class="streak-text">连败</span>
</div>
```

---

## 四、翻盘机制

### 绝境反击

当玩家连败 2 场时，提供翻盘机会：

1. **撤退重整**：返回地图，免费补充一个基础兵种
2. **背水一战**：下一场战斗胜利奖励 ×2，失败直接 Game Over

### 低保机制

连续失败 2 场后，下一场战斗：
- 敌人强度 -10%
- 胜利金币 +20%

---

## 五、实现代码（最终版本）

```javascript
// ========== Game Over 判定系统（连败淘汰制） ==========

function checkGameOver() {
    // 条件 1：连败≥3 场
    if (gameData.consecutiveLosses >= 3 && !gameData.gameOver) {
        gameData.gameOver = true;
        gameData.gameOverReason = 'consecutive_defeats';
        gameData.stats.endTime = Date.now();
        showGameOver();
        return true;
    }

    // 条件 2：金币<30 且无领地可征（返回地图时检查）
    if (gameData.gold < 30 && 
        gameData.defeatedTerritories.length >= gameData.targets.length && 
        !gameData.gameOver) {
        gameData.gameOver = true;
        gameData.gameOverReason = 'no_resources_no_land';
        gameData.stats.endTime = Date.now();
        showGameOver();
        return true;
    }

    // 预警系统（只在战斗中触发）
    if (gameData.inBattle) {
        // 连败 1 场警告
        if (gameData.consecutiveLosses === 1 && !gameData.warnedDefeatStreak1) {
            showToast('warning', '军心不稳', '连败 1 场，下一战请务必谨慎！');
            gameData.warnedDefeatStreak1 = true;
        }
        // 连败 2 场危险警告
        if (gameData.consecutiveLosses === 2 && !gameData.warnedDefeatStreak2) {
            showToast('error', '濒临崩溃', '再败一场，军团将溃散！');
            gameData.warnedDefeatStreak2 = true;
        }
    }

    return false;
}

// ========== 战斗结束处理 ==========
function finishBattleProcess(isVictory) {
    // ... 战斗统计 ...
    
    // 更新连败计数
    if (isVictory) {
        gameData.consecutiveLosses = 0; // 胜利重置连败
        checkVictory();
    } else {
        gameData.consecutiveLosses++; // 失败累加连败
    }

    // 战斗结束，退出战斗状态
    gameData.inBattle = false;

    // 战斗后检查 Game Over
    checkGameOver();
}

// ========== 招募/升级/侦察（不触发 Game Over） ==========
function recruitUnit(unitId) {
    const stats = getUnitStats(unitId);
    if (gameData.gold >= stats.cost) {
        // 正常招募
    } else {
        showToast('error', '金币不足', `需要 ${stats.cost} 金币`);
        // 不触发 Game Over
    }
}

function upgradeUnit(unitId) {
    const levelData = gameData.unitLevels[unitId];
    if (gameData.gold >= levelData.upgradeCost) {
        // 正常升级
    } else {
        showToast('error', '金币不足', `升级需要 ${levelData.upgradeCost} 金币`);
        // 不触发 Game Over
    }
}
```

---

## 六、数据结构更新

```javascript
gameData: {
    // 新增
    consecutiveLosses: 0,       // 当前连败场次
    warnedDefeatStreak1: false, // 连败 1 场警告
    warnedDefeatStreak2: false, // 连败 2 场警告
    inBattle: false,            // 是否在战斗中（控制预警触发）
    
    // 保留（旧系统遗留，已不使用）
    bankruptcyWarning: false,
    criticalWarning: false
}
```

---

## 七、Game Over 原因分类

| 原因代码 | 显示文本 | 触发条件 |
|----------|----------|----------|
| `consecutive_defeats` | 连战连败，军心溃散 | 连败 3 场 |
| `no_resources_no_land` | 资源耗尽，穷途末路 | 金币<30 且无领地可征 |
| `surrender` | 主动投降，虽败犹荣 | 玩家主动投降 |

---

## 八、测试场景

### 场景 1：招募失败
```
玩家有 30 金币，想招募 50 金币的步兵
→ 提示"金币不足"
→ 不触发 Game Over
→ 玩家可以返回地图征战
```

### 场景 2：连败 3 场
```
玩家连续征战失败 3 场
→ 第 3 场失败时触发 Game Over
→ 显示"连战连败，军心溃散"
```

### 场景 3：穷途末路
```
玩家金币 20，已征服所有 8 个领地
→ 返回地图时触发 Game Over
→ 显示"资源耗尽，穷途末路"
```

---

**总结**：Game Over 应该是对玩家**策略失误的惩罚**，而不是对**操作失败的阻断**。给玩家翻盘的机会，让失败更有意义。

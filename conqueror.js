const UNIT_DATA = {
    "步兵": {cost: 50, attack: 20, hp: 40, range: 1, color: "#4CAF50"},
    "弓兵": {cost: 100, attack: 20, hp: 30, range: 1, color: "#2196F3"},
    "盾兵": {cost: 150, attack: 20, hp: 50, range: 1, color: "#9E9E9E"},
    "矛兵": {cost: 150, attack: 60, hp: 60, range: 1, color: "#795548"},
    "枪兵": {cost: 200, attack: 60, hp: 60, range: 2, color: "#9C27B0"},
    "坦克": {cost: 250, attack: 80, hp: 100, range: 3, color: "#424242"},
};

const UNIT_LEVELS = {
    "步兵": [{attack: 20, hp: 40}, {attack: 40, hp: 60}, {attack: 70, hp: 80}, {attack: 90, hp: 100}],
    "弓兵": [{attack: 20, hp: 30, range: 1}, {attack: 40, hp: 60, range: 2}, {attack: 50, hp: 80, range: 3}, {attack: 60, hp: 100, range: 4}],
    "盾兵": [{attack: 20, hp: 50}, {attack: 40, hp: 100}, {attack: 60, hp: 120}, {attack: 100, hp: 200}],
    "矛兵": [{attack: 60, hp: 60}, {attack: 80, hp: 70}, {attack: 100, hp: 80}, {attack: 150, hp: 120}],
    "枪兵": [{attack: 60, hp: 60, range: 2}, {attack: 80, hp: 80, range: 3}, {attack: 100, hp: 100, range: 4}, {attack: 100, hp: 100, range: 4}],
    "坦克": [{attack: 80, hp: 100, range: 3}, {attack: 100, hp: 150, range: 4}, {attack: 120, hp: 200, range: 5}, {attack: 180, hp: 200, range: 6}],
};

const UPGRADE_COST = {
    "步兵": [250, 500, 750], "弓兵": [350, 700, 1050], "盾兵": [400, 800, 1200],
    "矛兵": [450, 900, 1350], "枪兵": [450, 900, 1350], "坦克": [500, 1000, 1500],
};

const UNLOCK_COST = { "盾兵": 200, "矛兵": 200, "枪兵": 250, "坦克": 300 };

let playerMoney = 500;
let ownedTerritories = [0];
let currentTarget = null;
let battleResult = null;
let canAttackAgain = false;
let defenseTimer = null;
let lastEnemyUnits = null;

let playerUnits = {
    "步兵": [1, 1, 1, 1, 1], "弓兵": [1, 1, 1],
    "盾兵": [], "矛兵": [], "枪兵": [], "坦克": [],
};

let unlockedUnits = { "步兵": true, "弓兵": true, "盾兵": false, "矛兵": false, "枪兵": false, "坦克": false };

const countryNames = ["北风国", "南疆国", "东海国", "西域国", "中原国", 
                     "云山国", "林海国", "雪原国", "沙漠国", "沼泽国",
                     "峡谷国", "平原国", "高原国", "半岛国", "岛国",
                     "草原国", "矿脉国", "渔港国", "商贸国", "边陲国"];

let countries = [];

function initCountries() {
    countries = [];
    const positions = [[150,150],[350,120],[550,150],[750,130],[950,160],
                     [200,300],[400,280],[600,320],[800,290],[1000,310],
                     [180,450],[380,430],[580,470],[780,440],[980,460],
                     [250,600],[450,580],[650,620],[850,590],[1050,610]];
    
    for (let i = 0; i < 20; i++) {
        const defenseUnits = {};
        const difficulty = Math.floor(Math.random() * 6) + 3;
        const available = ["步兵", "弓兵", "盾兵", "矛兵"];
        if (Math.random() > 0.5) available.push("枪兵");
        if (Math.random() > 0.7) available.push("坦克");
        
        for (let j = 0; j < difficulty; j++) {
            const unit = available[Math.floor(Math.random() * available.length)];
            const level = Math.floor(Math.random() * Math.min(3, 1 + i / 7)) + 1;
            if (!defenseUnits[unit]) defenseUnits[unit] = [];
            defenseUnits[unit].push(level);
        }
        
        countries.push({
            id: i, name: countryNames[i], x: positions[i][0], y: positions[i][1],
            color: `hsl(${Math.random() * 360}, 60%, 70%)`,
            owner: i === 0 ? 0 : null,
            tax: Math.floor(Math.random() * 100) + 50,
            defenseUnits: defenseUnits
        });
    }
}

function getUnitStats(name, level) {
    const base = UNIT_DATA[name];
    const levels = UNIT_LEVELS[name];
    if (levels && level <= levels.length) {
        const stats = levels[level - 1];
        return { attack: stats.attack, hp: stats.hp, range: stats.range || base.range };
    }
    return { attack: base.attack, hp: base.hp, range: base.range };
}

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function startGame() {
    initCountries();
    playerMoney = 500;
    ownedTerritories = [0];
    playerUnits = { "步兵": [1,1,1,1,1], "弓兵": [1,1,1], "盾兵": [], "矛兵": [], "枪兵": [], "坦克": [] };
    unlockedUnits = { "步兵": true, "弓兵": true, "盾兵": false, "矛兵": false, "枪兵": false, "坦克": false };
    updateMap();
    showScreen('map-screen');
}

function exitGame() { showScreen('menu-screen'); }

function updateMap() {
    document.getElementById('money-display').textContent = playerMoney;
    document.getElementById('territory-display').textContent = ownedTerritories.length;
    
    const mapArea = document.getElementById('map-area');
    mapArea.innerHTML = '';
    
    countries.forEach(country => {
        const el = document.createElement('div');
        el.className = 'country';
        el.style.left = (country.x - 60) + 'px';
        el.style.top = (country.y - 50) + 'px';
        el.style.width = '120px';
        el.style.height = '100px';
        
        const bgColor = country.owner === 0 ? '#4CAF50' : (country.owner === null ? country.color : '#f44336');
        
        el.innerHTML = `
            <svg width="120" height="100" style="position:absolute;top:0;left:0;">
                <polygon points="60,10 110,30 100,80 50,90 10,60 20,20" 
                         fill="${bgColor}" stroke="#333" stroke-width="2"/>
            </svg>
            <div class="country-name" style="left:30px;top:35px;width:60px;">${country.name}</div>
            <div class="country-tax" style="left:30px;top:55px;width:60px;">税:${country.tax}</div>
        `;
        
        if (country.owner !== 0) {
            el.onclick = () => selectCountry(country.id);
        }
        mapArea.appendChild(el);
    });
}

function selectCountry(id) {
    currentTarget = id;
    document.getElementById('target-name').textContent = '攻打 ' + countries[id].name;
    updateRecruitScreen();
    showScreen('recruit-screen');
}

function updateRecruitScreen() {
    document.getElementById('recruit-money').textContent = playerMoney;
    
    const enemyForces = countries[currentTarget].defenseUnits;
    let enemyHtml = '';
    for (let [unit, levels] of Object.entries(enemyForces)) {
        enemyHtml += `<div>${unit}: ${levels.sort().map(l => l + '级').join(',')}</div>`;
    }
    document.getElementById('enemy-forces').innerHTML = enemyHtml || '<div>无</div>';
    
    let allyHtml = '';
    for (let [unit, levels] of Object.entries(playerUnits)) {
        if (levels.length > 0) {
            const counts = {};
            levels.forEach(l => counts[l] = (counts[l] || 0) + 1);
            const parts = Object.entries(counts).map(([lvl, cnt]) => `${lvl}级x${cnt}`);
            allyHtml += `<div>${unit}: ${parts.join(', ')}</div>`;
        }
    }
    document.getElementById('ally-forces').innerHTML = allyHtml || '<div>无</div>';
    
    const shop = document.getElementById('unit-shop');
    shop.innerHTML = '';
    
    for (let [name, data] of Object.entries(UNIT_DATA)) {
        const isUnlocked = unlockedUnits[name];
        const card = document.createElement('div');
        card.className = 'unit-card' + (isUnlocked ? '' : ' locked');
        
        if (isUnlocked) {
            const stats = getUnitStats(name, 1);
            const counts = {};
            playerUnits[name].forEach(l => counts[l] = (counts[l] || 0) + 1);
            const parts = Object.entries(counts).map(([lvl, cnt]) => `${lvl}级x${cnt}`);
            
            card.innerHTML = `
                <h4 style="color:${data.color}">${name}</h4>
                <div class="unit-stats">价格:${data.cost} 攻:${stats.attack} 血:${stats.hp} 射程:${stats.range}</div>
                <div class="unit-owned">拥有: ${parts.join(', ') || '无'}</div>
                <button class="btn btn-green" onclick="buyUnit('${name}')" ${playerMoney < data.cost ? 'disabled' : ''}>购买</button>
            `;
        } else {
            card.innerHTML = `
                <h4 style="color:#999">${name}</h4>
                <div class="unit-stats">[未解锁]</div>
                <div class="unit-owned">解锁需${UNLOCK_COST[name]}元</div>
                <button class="btn" disabled>未解锁</button>
            `;
        }
        shop.appendChild(card);
    }
    
    const hasUnits = Object.values(playerUnits).some(arr => arr.length > 0);
    document.getElementById('attack-btn').disabled = !hasUnits;
}

function buyUnit(name) {
    const cost = UNIT_DATA[name].cost;
    if (playerMoney >= cost) {
        playerMoney -= cost;
        playerUnits[name].push(1);
        updateRecruitScreen();
    }
}

function backToMap() {
    currentTarget = null;
    canAttackAgain = false;
    if (defenseTimer) clearInterval(defenseTimer);
    updateMap();
    showScreen('map-screen');
}

function backToRecruit() {
    updateRecruitScreen();
    showScreen('recruit-screen');
}

function showUnlock() {
    document.getElementById('unlock-money').textContent = playerMoney;
    const grid = document.getElementById('unlock-grid');
    grid.innerHTML = '';
    
    for (let [name, cost] of Object.entries(UNLOCK_COST)) {
        const isUnlocked = unlockedUnits[name];
        const card = document.createElement('div');
        card.className = 'unlock-card' + (isUnlocked ? ' unlocked' : '');
        
        if (isUnlocked) {
            card.innerHTML = `<h3>${name}</h3><div style="font-size:24px;color:#4CAF50;">✓ 已解锁</div>`;
        } else {
            card.innerHTML = `
                <h3>${name}</h3>
                <div class="unlock-cost">需要 ${cost} 元</div>
                <button class="btn btn-yellow" onclick="unlockUnit('${name}')" ${playerMoney < cost ? 'disabled' : ''}>解锁</button>
            `;
        }
        grid.appendChild(card);
    }
    showScreen('unlock-screen');
}

function unlockUnit(name) {
    const cost = UNLOCK_COST[name];
    if (playerMoney >= cost) {
        playerMoney -= cost;
        unlockedUnits[name] = true;
        showUnlock();
    }
}

function showUpgrade() {
    document.getElementById('upgrade-money').textContent = playerMoney;
    const grid = document.getElementById('upgrade-grid');
    grid.innerHTML = '';
    
    for (let name of Object.keys(UNIT_DATA)) {
        const card = document.createElement('div');
        card.className = 'upgrade-card';
        
        const counts = {};
        playerUnits[name].forEach(l => counts[l] = (counts[l] || 0) + 1);
        
        let levelsHtml = '';
        for (let lvl = 1; lvl <= 4; lvl++) {
            if (counts[lvl]) {
                const stats = getUnitStats(name, lvl);
                levelsHtml += `<div>${lvl}级x${counts[lvl]}: 攻${stats.attack} 血${stats.hp}</div>`;
            }
        }
        
        let upgradeBtn = '';
        for (let lvl = 1; lvl <= 3; lvl++) {
            if (counts[lvl] > 0) {
                const cost = UPGRADE_COST[name][lvl - 1];
                upgradeBtn = `<button class="btn btn-blue" onclick="upgradeUnit('${name}', ${lvl})" ${playerMoney < cost ? 'disabled' : ''}>升${lvl+1}级 (${cost}元)</button>`;
                break;
            }
        }
        
        card.innerHTML = `
            <h3>${name}</h3>
            <div class="upgrade-levels">${levelsHtml || '未拥有该兵种'}</div>
            ${upgradeBtn}
        `;
        grid.appendChild(card);
    }
    showScreen('upgrade-screen');
}

function upgradeUnit(name, fromLevel) {
    const cost = UPGRADE_COST[name][fromLevel - 1];
    if (playerMoney >= cost) {
        const idx = playerUnits[name].indexOf(fromLevel);
        if (idx !== -1) {
            playerMoney -= cost;
            playerUnits[name][idx] = fromLevel + 1;
            showUpgrade();
        }
    }
}

function startBattle() {
    battleResult = null;
    document.getElementById('battle-log').innerHTML = '';
    document.getElementById('battle-result').innerHTML = '';
    document.getElementById('battle-actions').style.display = 'block';
    showScreen('battle-screen');
}

function flattenUnits(unitsDict) {
    const result = [];
    for (let [name, levels] of Object.entries(unitsDict)) {
        for (let level of levels) {
            const stats = getUnitStats(name, level);
            result.push({ name, level, maxHp: stats.hp, hp: stats.hp, attack: stats.attack, range: stats.range });
        }
    }
    return result;
}

function autoBattle() {
    const enemyUnits = countries[currentTarget].defenseUnits;
    let attackers = flattenUnits(playerUnits);
    let defenders = flattenUnits(enemyUnits);
    
    const logDiv = document.getElementById('battle-log');
    let log = [];
    
    for (let turn = 0; turn < 50; turn++) {
        for (let unit of attackers.filter(u => u.hp > 0)) {
            const aliveDefenders = defenders.filter(d => d.hp > 0);
            if (aliveDefenders.length === 0) break;
            
            const target = aliveDefenders[0];
            const damage = unit.attack;
            target.hp -= damage;
            log.push(`我方${unit.name}Lv${unit.level} 攻击 敌方${target.name}Lv${target.level} 造成${damage}伤害`);
            
            if (target.hp <= 0) {
                log.push(`  -> 敌方${target.name}Lv${target.level} 被击败!`);
            }
        }
        
        if (defenders.every(d => d.hp <= 0)) {
            battleResult = 'win';
            break;
        }
        
        for (let unit of defenders.filter(u => u.hp > 0)) {
            const aliveAttackers = attackers.filter(a => a.hp > 0);
            if (aliveAttackers.length === 0) break;
            
            const target = aliveAttackers[0];
            const damage = unit.attack;
            target.hp -= damage;
            log.push(`敌方${unit.name}Lv${unit.level} 攻击 我方${target.name}Lv${target.level} 造成${damage}伤害`);
            
            if (target.hp <= 0) {
                log.push(`  -> 我方${target.name}Lv${target.level} 被击败!`);
            }
        }
        
        if (attackers.every(a => a.hp <= 0)) {
            battleResult = 'lose';
            break;
        }
    }
    
    if (!battleResult) {
        const attackerPower = attackers.filter(a => a.hp > 0).reduce((s, u) => s + u.hp, 0);
        const defenderPower = defenders.filter(d => d.hp > 0).reduce((s, u) => s + u.hp, 0);
        battleResult = attackerPower > defenderPower ? 'win' : (attackerPower === defenderPower ? 'draw' : 'lose');
    }
    
    logDiv.innerHTML = log.slice(-20).map(l => `<div>${l}</div>`).join('');
    logDiv.scrollTop = logDiv.scrollHeight;
    
    document.getElementById('battle-actions').style.display = 'none';
    const resultDiv = document.getElementById('battle-result');
    
    if (battleResult === 'win') {
        const reward = Math.floor(Math.random() * 501) + 500;
        playerMoney += reward + countries[currentTarget].tax;
        countries[currentTarget].owner = 0;
        if (!ownedTerritories.includes(currentTarget)) ownedTerritories.push(currentTarget);
        resultDiv.innerHTML = `<div class="win">胜利！</div><div style="font-size:24px;margin-top:20px;">获得 ${reward} 元 + 税收 ${countries[currentTarget].tax}</div><button class="btn btn-green" onclick="backToMap()" style="margin-top:30px;">返回地图</button>`;
    } else if (battleResult === 'draw') {
        resultDiv.innerHTML = `<div class="draw">平局</div><button class="btn btn-gray" onclick="backToMap()" style="margin-top:30px;">返回地图</button>`;
    } else {
        lastEnemyUnits = JSON.parse(JSON.stringify(countries[currentTarget].defenseUnits));
        resultDiv.innerHTML = `<div class="lose">失败！</div><button class="btn btn-red" onclick="showDefense()" style="margin-top:30px;">进入防守战</button>`;
    }
}

function showDefense() {
    let enemyHtml = '';
    for (let [unit, levels] of Object.entries(lastEnemyUnits)) {
        const counts = {};
        levels.forEach(l => counts[l] = (counts[l] || 0) + 1);
        const parts = Object.entries(counts).map(([lvl, cnt]) => `${lvl}级x${cnt}`);
        enemyHtml += `<div>${unit}: ${parts.join(', ')}</div>`;
    }
    document.getElementById('defense-enemy').innerHTML = enemyHtml || '<div>无</div>';
    
    let allyHtml = '';
    for (let [unit, levels] of Object.entries(playerUnits)) {
        if (levels.length > 0) {
            const counts = {};
            levels.forEach(l => counts[l] = (counts[l] || 0) + 1);
            const parts = Object.entries(counts).map(([lvl, cnt]) => `${lvl}级x${cnt}`);
            allyHtml += `<div>${unit}: ${parts.join(', ')}</div>`;
        }
    }
    document.getElementById('defense-ally').innerHTML = allyHtml || '<div>无</div>';
    
    showScreen('defense-screen');
}

function startDefense() {
    let attackers = flattenUnits(playerUnits);
    let defenders = flattenUnits(lastEnemyUnits);
    
    for (let turn = 0; turn < 50; turn++) {
        for (let unit of attackers.filter(u => u.hp > 0)) {
            const aliveDefenders = defenders.filter(d => d.hp > 0);
            if (aliveDefenders.length === 0) break;
            const target = aliveDefenders[0];
            target.hp -= unit.attack;
        }
        
        if (defenders.every(d => d.hp <= 0)) {
            defenseWin();
            return;
        }
        
        for (let unit of defenders.filter(u => u.hp > 0)) {
            const aliveAttackers = attackers.filter(a => a.hp > 0);
            if (aliveAttackers.length === 0) break;
            const target = aliveAttackers[0];
            target.hp -= unit.attack;
        }
        
        if (attackers.every(a => a.hp <= 0)) {
            defenseLose();
            return;
        }
    }
    
    const attackerPower = attackers.filter(a => a.hp > 0).reduce((s, u) => s + u.hp, 0);
    const defenderPower = defenders.filter(d => d.hp > 0).reduce((s, u) => s + u.hp, 0);
    if (attackerPower >= defenderPower) {
        defenseWin();
    } else {
        defenseLose();
    }
}

function defenseWin() {
    const reward = Math.floor(Math.random() * 300) + 200;
    playerMoney += reward;
    countries[currentTarget].tax = Math.floor(countries[currentTarget].tax / 2);
    
    document.getElementById('result-title').textContent = '防守胜利！';
    document.getElementById('result-title').style.color = '#4CAF50';
    document.getElementById('result-message').textContent = `获得 ${reward} 元和半块地！`;
    
    canAttackAgain = true;
    let timeLeft = 5;
    document.getElementById('timer-display').textContent = `${timeLeft}秒内可再次进攻`;
    
    defenseTimer = setInterval(() => {
        timeLeft--;
        if (timeLeft > 0) {
            document.getElementById('timer-display').textContent = `${timeLeft}秒内可再次进攻`;
        } else {
            clearInterval(defenseTimer);
            canAttackAgain = false;
            document.getElementById('timer-display').textContent = '进攻时机已错过';
            document.getElementById('result-actions').innerHTML = '<button class="btn btn-gray" onclick="backToMap()">返回地图</button>';
        }
    }, 1000);
    
    document.getElementById('result-actions').innerHTML = `
        <button class="btn btn-red" onclick="attackAgain()">再次进攻</button>
        <button class="btn btn-gray" onclick="backToMap()">返回地图</button>
    `;
    
    showScreen('result-screen');
}

function defenseLose() {
    document.getElementById('result-title').textContent = '防守失败...';
    document.getElementById('result-title').style.color = '#f44336';
    document.getElementById('result-message').textContent = '你的领土被攻陷了';
    document.getElementById('timer-display').textContent = '';
    document.getElementById('result-actions').innerHTML = '<button class="btn btn-gray" onclick="backToMap()">返回地图</button>';
    showScreen('result-screen');
}

function attackAgain() {
    if (canAttackAgain) {
        clearInterval(defenseTimer);
        showScreen('recruit-screen');
        updateRecruitScreen();
    }
}
// ==================== 游戏配置 ====================
const CONFIG = {
    units: {
        步兵: { cost: 50, attack: 20, hp: 40, range: 1, color: '#4CAF50' },
        弓兵: { cost: 100, attack: 20, hp: 30, range: 1, color: '#2196F3' },
        盾兵: { cost: 150, attack: 20, hp: 50, range: 1, color: '#9E9E9E' },
        矛兵: { cost: 150, attack: 60, hp: 60, range: 1, color: '#795548' },
        枪兵: { cost: 200, attack: 60, hp: 60, range: 2, color: '#9C27B0' },
        坦克: { cost: 250, attack: 80, hp: 100, range: 3, color: '#424242' }
    },
    levels: {
        步兵: [{a:20,h:40},{a:40,h:60},{a:70,h:80},{a:90,h:100}],
        弓兵: [{a:20,h:30,r:1},{a:40,h:60,r:2},{a:50,h:80,r:3},{a:60,h:100,r:4}],
        盾兵: [{a:20,h:50},{a:40,h:100},{a:60,h:120},{a:100,h:200}],
        矛兵: [{a:60,h:60},{a:80,h:70},{a:100,h:80},{a:150,h:120}],
        枪兵: [{a:60,h:60,r:2},{a:80,h:80,r:3},{a:100,h:100,r:4},{a:100,h:100,r:4}],
        坦克: [{a:80,h:100,r:3},{a:100,h:150,r:4},{a:120,h:200,r:5},{a:180,h:200,r:6}]
    },
    upgradeCost: {
        步兵: [250,500,750], 弓兵: [350,700,1050], 盾兵: [400,800,1200],
        矛兵: [450,900,1350], 枪兵: [450,900,1350], 坦克: [500,1000,1500]
    },
    unlockCost: { 盾兵:200, 矛兵:200, 枪兵:250, 坦克:300 },
    countryNames: ['北风国','南疆国','东海国','西域国','中原国','云山国','林海国','雪原国','沙漠国','沼泽国',
                   '峡谷国','平原国','高原国','半岛国','岛国','草原国','矿脉国','渔港国','商贸国','边陲国'],
    positions: (() => {
        // 生成紧密排列的4行5列网格，间隔2px
        const pos = [];
        const startX = 80, startY = 60;
        const gapX = 102, gapY = 82; // 100px国家宽度 + 2px间隔
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 5; col++) {
                pos.push([
                    startX + col * gapX + (row % 2) * 50, // 奇数行偏移，形成蜂窝状
                    startY + row * gapY
                ]);
            }
        }
        return pos;
    })()
};

// ==================== 游戏主类 ====================
class Game {
    constructor() {
        this.reset();
    }
    
    reset() {
        this.money = 500;
        this.territories = [0];
        this.units = { 步兵:[1,1,1,1,1], 弓兵:[1,1,1], 盾兵:[], 矛兵:[], 枪兵:[], 坦克:[] };
        this.unlocked = { 步兵:true, 弓兵:true, 盾兵:false, 矛兵:false, 枪兵:false, 坦克:false };
        this.countries = [];
        this.targetId = null;
        this.lastEnemy = null;
        this.timer = null;
        this.canAttackAgain = false;
    }
    
    getStats(name, level) {
        const base = CONFIG.units[name];
        const lv = CONFIG.levels[name][level-1];
        return { attack: lv.a, hp: lv.h, range: lv.r || base.range };
    }
    
    flatten(units) {
        const res = [];
        for (let [name, levels] of Object.entries(units)) {
            for (let lv of levels) {
                const s = this.getStats(name, lv);
                res.push({ name, level: lv, hp: s.hp, maxHp: s.hp, attack: s.attack });
            }
        }
        return res;
    }
    
    genCountries() {
        this.countries = CONFIG.positions.map((pos, i) => {
            const defense = {};
            const diff = Math.floor(Math.random() * 6) + 3;
            const avail = ['步兵','弓兵','盾兵','矛兵'];
            if (Math.random() > 0.5) avail.push('枪兵');
            if (Math.random() > 0.7) avail.push('坦克');
            for (let j = 0; j < diff; j++) {
                const u = avail[Math.floor(Math.random() * avail.length)];
                const lv = Math.floor(Math.random() * Math.min(3, 1 + i / 7)) + 1;
                defense[u] = defense[u] || [];
                defense[u].push(lv);
            }
            return { id: i, name: CONFIG.countryNames[i], x: pos[0], y: pos[1],
                     color: `hsl(${Math.random()*360},60%,50%)`, owner: i===0?0:null,
                     tax: Math.floor(Math.random()*100)+50, defense };
        });
    }
    
    show(id) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }
    
    start() {
        this.reset();
        this.genCountries();
        this.renderMap();
        this.show('map-screen');
    }
    
    exit() { this.show('menu-screen'); }
    
    renderMap() {
        document.getElementById('stat-money').textContent = this.money;
        document.getElementById('stat-territory').textContent = this.territories.length;
        const isMobile = window.innerWidth <= 768;
        const area = document.getElementById(isMobile ? 'map-wrapper' : 'map-area');
        if (isMobile) {
            document.getElementById('map-area').style.overflow = 'auto';
            document.getElementById('map-wrapper').style.width = '650px';
            document.getElementById('map-wrapper').style.height = '400px';
        }
        area.innerHTML = '';
        this.countries.forEach(c => {
            const el = document.createElement('div');
            el.className = 'country ' + (c.owner===0 ? 'country-owned' : 'country-neutral');
            el.style.left = c.x + 'px';
            el.style.top = c.y + 'px';
            el.innerHTML = `<div class="country-shape">${c.name}</div><div class="country-tax">税:${c.tax}</div>`;
            if (c.owner !== 0) el.onclick = () => this.selectCountry(c.id);
            area.appendChild(el);
        });
    }
    
    selectCountry(id) {
        this.targetId = id;
        document.getElementById('target-title').textContent = `准备攻打 ${this.countries[id].name}`;
        this.renderRecruit();
        this.show('recruit-screen');
    }
    
    renderForceList(units) {
        let html = '';
        for (let [n, lvs] of Object.entries(units)) {
            if (!lvs.length) continue;
            const cnt = {};
            lvs.forEach(l => cnt[l] = (cnt[l]||0)+1);
            html += `<div>${n}: ${Object.entries(cnt).map(([l,c])=>`${l}级x${c}`).join(', ')}</div>`;
        }
        return html || '无';
    }
    
    renderRecruit() {
        document.getElementById('shop-money').textContent = this.money;
        const target = this.countries[this.targetId];
        document.getElementById('enemy-forces').innerHTML = this.renderForceList(target.defense);
        document.getElementById('ally-forces').innerHTML = this.renderForceList(this.units);
        
        const shop = document.getElementById('unit-shop');
        shop.innerHTML = '';
        for (let [n, d] of Object.entries(CONFIG.units)) {
            const card = document.createElement('div');
            card.className = 'unit-card' + (this.unlocked[n]?'':' locked');
            if (this.unlocked[n]) {
                const s = this.getStats(n, 1);
                const cnt = {};
                this.units[n].forEach(l => cnt[l] = (cnt[l]||0)+1);
                const parts = Object.entries(cnt).map(([l,c])=>`${l}级x${c}`);
                card.innerHTML = `<h4 style="color:${d.color}">${n}</h4><div class="unit-stats">价格:${d.cost} 攻:${s.attack} 血:${s.hp} 射程:${s.range}</div><div class="unit-owned">${parts.join(', ')||'未拥有'}</div><button class="btn btn-green" onclick="game.buyUnit('${n}')" ${this.money<d.cost?'disabled':''}>购买</button>`;
            } else {
                card.innerHTML = `<h4 style="color:#666">${n}</h4><div class="unlock-cost">解锁需 ${CONFIG.unlockCost[n]} 元</div><button class="btn" disabled>未解锁</button>`;
            }
            shop.appendChild(card);
        }
        document.getElementById('btn-attack').disabled = !Object.values(this.units).some(a=>a.length>0);
    }
    
    buyUnit(n) {
        const c = CONFIG.units[n].cost;
        if (this.money >= c) {
            this.money -= c;
            this.units[n].push(1);
            this.renderRecruit();
        }
    }
    
    toMap() {
        this.targetId = null;
        if (this.timer) clearInterval(this.timer);
        this.renderMap();
        this.show('map-screen');
    }
    
    toRecruit() { this.renderRecruit(); this.show('recruit-screen'); }
    
    toUnlock() {
        document.getElementById('unlock-money').textContent = this.money;
        const list = document.getElementById('unlock-list');
        list.innerHTML = '';
        for (let [n, c] of Object.entries(CONFIG.unlockCost)) {
            const card = document.createElement('div');
            card.className = 'card' + (this.unlocked[n]?' unlocked':'');
            card.innerHTML = this.unlocked[n] ? `<h3>${n}</h3><div style="color:#4CAF50;font-size:24px;">✓ 已解锁</div>` : `<h3>${n}</h3><div class="cost">${c} 元</div><button class="btn btn-yellow" onclick="game.unlock('${n}')" ${this.money<c?'disabled':''}>解锁</button>`;
            list.appendChild(card);
        }
        this.show('unlock-screen');
    }
    
    unlock(n) {
        const c = CONFIG.unlockCost[n];
        if (this.money >= c) {
            this.money -= c;
            this.unlocked[n] = true;
            this.toUnlock();
        }
    }
    
    toUpgrade() {
        document.getElementById('upgrade-money').textContent = this.money;
        const list = document.getElementById('upgrade-list');
        list.innerHTML = '';
        for (let n of Object.keys(CONFIG.units)) {
            const card = document.createElement('div');
            card.className = 'card';
            const cnt = {};
            this.units[n].forEach(l => cnt[l] = (cnt[l]||0)+1);
            let lvHtml = '';
            for (let l = 1; l <= 4; l++) {
                if (cnt[l]) {
                    const s = this.getStats(n, l);
                    lvHtml += `<div>${l}级x${cnt[l]}: 攻${s.attack} 血${s.hp}</div>`;
                }
            }
            let btn = '';
            for (let l = 1; l <= 3; l++) {
                if (cnt[l]) {
                    const cost = CONFIG.upgradeCost[n][l-1];
                    btn = `<button class="btn btn-blue" onclick="game.upgrade('${n}',${l})" ${this.money<cost?'disabled':''}>升${l+1}级 (${cost}元)</button>`;
                    break;
                }
            }
            card.innerHTML = `<h3 style="color:${CONFIG.units[n].color}">${n}</h3><div class="desc">${lvHtml||'未拥有'}</div>${btn}`;
            list.appendChild(card);
        }
        this.show('upgrade-screen');
    }
    
    upgrade(n, from) {
        const cost = CONFIG.upgradeCost[n][from-1];
        if (this.money >= cost) {
            const idx = this.units[n].indexOf(from);
            if (idx !== -1) {
                this.money -= cost;
                this.units[n][idx] = from + 1;
                this.toUpgrade();
            }
        }
    }
    
    startAttack() {
        this.lastEnemy = JSON.parse(JSON.stringify(this.countries[this.targetId].defense));
        this.runBattle(this.units, this.countries[this.targetId].defense, 'attack');
    }
    
    showDefense() {
        document.getElementById('defense-enemy').innerHTML = this.renderForceList(this.lastEnemy);
        document.getElementById('defense-ally').innerHTML = this.renderForceList(this.units);
        this.show('defense-screen');
    }
    
    runDefense() {
        this.runBattle(this.units, this.lastEnemy, 'defense');
    }
    
    runBattle(allyDict, enemyDict, type) {
        let ally = this.flatten(allyDict);
        let enemy = this.flatten(enemyDict);
        const logDiv = document.getElementById('battle-log');
        const resultDiv = document.getElementById('battle-result');
        const actionsDiv = document.getElementById('battle-actions');
        
        logDiv.innerHTML = '';
        resultDiv.innerHTML = '';
        actionsDiv.style.display = 'block';
        this.show('battle-screen');
        
        // 保存当前战斗状态用于按钮回调
        this.currentBattle = { ally, enemy, type };
    }
    
    // 执行战斗（按钮调用）
    executeBattle() {
        if (!this.currentBattle) return;
        
        let { ally, enemy, type } = this.currentBattle;
        const logDiv = document.getElementById('battle-log');
        const resultDiv = document.getElementById('battle-result');
        const actionsDiv = document.getElementById('battle-actions');
        
        let log = [];
        let result = null;
        
        for (let turn = 0; turn < 50; turn++) {
            for (let u of ally.filter(x=>x.hp>0)) {
                const targets = enemy.filter(x=>x.hp>0);
                if (!targets.length) break;
                const t = targets[0];
                t.hp -= u.attack;
                log.push(`<span style="color:#4CAF50">我方${u.name}Lv${u.level}</span> 攻击 <span style="color:#f44336">敌方${t.name}Lv${t.level}</span> 造成${u.attack}伤害`);
                if (t.hp <= 0) log.push(`<span style="color:#FFC107">  → 敌方${t.name}Lv${t.level} 被击败!</span>`);
            }
            if (enemy.every(x=>x.hp<=0)) { result = 'win'; break; }
            
            for (let u of enemy.filter(x=>x.hp>0)) {
                const targets = ally.filter(x=>x.hp>0);
                if (!targets.length) break;
                const t = targets[0];
                t.hp -= u.attack;
                log.push(`<span style="color:#f44336">敌方${u.name}Lv${u.level}</span> 攻击 <span style="color:#4CAF50">我方${t.name}Lv${t.level}</span> 造成${u.attack}伤害`);
                if (t.hp <= 0) log.push(`<span style="color:#FFC107">  → 我方${t.name}Lv${t.level} 被击败!</span>`);
            }
            if (ally.every(x=>x.hp<=0)) { result = 'lose'; break; }
        }
        
        if (!result) {
            const aHp = ally.filter(x=>x.hp>0).reduce((s,x)=>s+x.hp,0);
            const eHp = enemy.filter(x=>x.hp>0).reduce((s,x)=>s+x.hp,0);
            result = aHp > eHp ? 'win' : (aHp < eHp ? 'lose' : 'draw');
        }
        
        logDiv.innerHTML = log.slice(-20).join('<br>');
        logDiv.scrollTop = logDiv.scrollHeight;
        actionsDiv.style.display = 'none';
        
        if (type === 'attack') {
            if (result === 'win') {
                const reward = Math.floor(Math.random() * 501) + 500;
                this.money += reward + this.countries[this.targetId].tax;
                this.countries[this.targetId].owner = 0;
                if (!this.territories.includes(this.targetId)) this.territories.push(this.targetId);
                resultDiv.innerHTML = `<div class="result-win">进攻胜利！</div><div style="font-size:20px;margin-top:15px;">获得 ${reward} 元 + 税收 ${this.countries[this.targetId].tax}</div><button class="btn btn-green" onclick="game.toMap()" style="margin-top:20px;">返回地图</button>`;
            } else if (result === 'draw') {
                resultDiv.innerHTML = `<div class="result-draw">平局</div><button class="btn btn-gray" onclick="game.toMap()" style="margin-top:20px;">返回地图</button>`;
            } else {
                resultDiv.innerHTML = `<div class="result-lose">进攻失败！</div><button class="btn btn-red" onclick="game.showDefense()" style="margin-top:20px;">进入防守战</button>`;
            }
        } else {
            if (result === 'win' || result === 'draw') {
                const reward = Math.floor(Math.random() * 301) + 200;
                this.money += reward;
                this.countries[this.targetId].tax = Math.floor(this.countries[this.targetId].tax / 2);
                this.showDefenseWin(reward);
            } else {
                this.showDefenseLose();
            }
        }
        
        this.currentBattle = null;
    }
    
    showDefenseWin(reward) {
        document.getElementById('result-title').textContent = '防守胜利！';
        document.getElementById('result-title').style.color = '#4CAF50';
        document.getElementById('result-message').textContent = `获得 ${reward} 元和半块地！`;
        this.canAttackAgain = true;
        let timeLeft = 5;
        document.getElementById('timer-display').textContent = `${timeLeft}秒内可再次进攻`;
        document.getElementById('result-actions').innerHTML = `<button class="btn btn-red" onclick="game.attackAgain()">再次进攻</button><button class="btn btn-gray" onclick="game.toMap()">返回地图</button>`;
        this.show('result-screen');
        
        this.timer = setInterval(() => {
            timeLeft--;
            if (timeLeft > 0) {
                document.getElementById('timer-display').textContent = `${timeLeft}秒内可再次进攻`;
            } else {
                clearInterval(this.timer);
                this.canAttackAgain = false;
                document.getElementById('timer-display').textContent = '进攻时机已错过';
                document.getElementById('result-actions').innerHTML = '<button class="btn btn-gray" onclick="game.toMap()">返回地图</button>';
            }
        }, 1000);
    }
    
    showDefenseLose() {
        document.getElementById('result-title').textContent = '防守失败...';
        document.getElementById('result-title').style.color = '#f44336';
        document.getElementById('result-message').textContent = '你的领土被攻陷了';
        document.getElementById('timer-display').textContent = '';
        document.getElementById('result-actions').innerHTML = '<button class="btn btn-gray" onclick="game.toMap()">返回地图</button>';
        this.show('result-screen');
    }
    
    attackAgain() {
        if (this.canAttackAgain) {
            clearInterval(this.timer);
            this.toRecruit();
        }
    }
}

const game = new Game();

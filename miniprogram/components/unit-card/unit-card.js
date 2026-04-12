// components/unit-card/unit-card.js
Component({
  properties: {
    icon: {
      type: String,
      value: ''
    },
    name: {
      type: String,
      value: ''
    },
    attack: {
      type: Number,
      value: 0
    },
    hp: {
      type: Number,
      value: 0
    },
    maxHp: {
      type: Number,
      value: 0
    },
    cost: {
      type: Number,
      value: 0
    },
    level: {
      type: Number,
      value: 1
    },
    unlocked: {
      type: Boolean,
      value: true
    },
    unlockCost: {
      type: Number,
      value: 0
    },
    type: {
      type: String,
      value: 'player' // player, enemy
    },
    disabled: {
      type: Boolean,
      value: false
    }
  },

  methods: {
    handleTap() {
      if (!this.data.disabled) {
        this.triggerEvent('tap');
      }
    }
  }
});

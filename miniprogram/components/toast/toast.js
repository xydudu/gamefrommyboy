// components/toast/toast.js
Component({
  properties: {
    show: {
      type: Boolean,
      value: false
    },
    type: {
      type: String,
      value: 'info' // info, warning, error, success
    },
    title: {
      type: String,
      value: ''
    },
    message: {
      type: String,
      value: ''
    },
    duration: {
      type: Number,
      value: 2000
    }
  },

  data: {
    icon: 'ℹ️'
  },

  observers: {
    show: function(newVal) {
      if (newVal) {
        this.updateIcon();
        this.autoHide();
      }
    }
  },

  methods: {
    updateIcon() {
      const icons = {
        info: 'ℹ️',
        warning: '⚠️',
        error: '❌',
        success: '✅'
      };
      this.setData({
        icon: icons[this.data.type] || icons.info
      });
    },

    autoHide() {
      if (this.data.duration > 0) {
        setTimeout(() => {
          this.hideToast();
        }, this.data.duration);
      }
    },

    hideToast() {
      this.triggerEvent('hide');
    }
  }
});

// app.js
App({
    onLaunch: function () {
        this.wxLogin();
    },

    wxLogin: function () {
        // 微信登录
        wx.login({
            success: res => {
                if (res.code) {
                    this.getTokenFromBackend(res.code);
                } else {
                    wx.showToast({
                        title: '登录失败！' + res.errMsg,
                    })
                }
            }
        });
    },

    getTokenFromBackend: function (code) {
        wx.request({
            url: 'http://localhost:8000/api/users/wx_login/',
            method: 'POST',
            data: {
                code: code
            },
            success: res => {
                if (res.data && res.data.user && res.data.tokens) {
                    this.globalData.userInfo = res.data.user;
                    this.globalData.tokens = res.data.tokens;

                    console.log(res);

                    wx.setStorageSync('userInfo', res.data.user);
                    wx.setStorageSync('tokens', res.data.tokens);

                    wx.showToast({
                        title: '登录成功',
                    })
                }
            },
            fail: err => {
                wx.showToast({
                    title: '登录失败',
                })
            }
        });
    },

    globalData: {
        userInfo: null,
        tokens: null
    }
});
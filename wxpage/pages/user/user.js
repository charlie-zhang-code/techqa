import { getUserInfo, getQuestions, getUserAnswers, getMyVote } from '../../utils/request';

Page({
  data: {
    userInfo: null,
    stats: {
      questionsCount: 0,
      answersCount: 0,
      votesCount: 0,
      reputation: 0
    },
    isLoading: true
  },

  onLoad() {
    this.loadUserData();
  },

  onShow() {
    // 每次显示页面时刷新数据
    this.loadUserData();
  },

  loadUserData() {
    const userInfo = wx.getStorageSync('userInfo');
    if (!userInfo) {
      wx.redirectTo({
        url: '/pages/login/login'
      });
      return;
    }

    this.setData({
      userInfo,
      isLoading: true
    });

    Promise.all([
      getQuestions({ author: userInfo.id, page_size: 1 }), // 只获取数量
      getUserAnswers({ author: userInfo.id, page_size: 1 }), // 只获取数量
      getMyVote()
    ]).then(([questionsRes, answersRes, votesRes]) => {
      this.setData({
        stats: {
          questionsCount: questionsRes.count || questionsRes.length || 0,
          answersCount: answersRes.count || answersRes.length || 0,
          votesCount: votesRes.length || 0,
          reputation: userInfo.reputation || 0
        },
        isLoading: false
      });
    }).catch(err => {
      console.error('加载用户数据失败:', err);
      this.setData({ isLoading: false });
      wx.showToast({
        title: '加载数据失败',
        icon: 'none'
      });
    });
  },

  navigateToMyQuestions() {
    wx.navigateTo({
      url: '/pages/user/questions'
    });
  },

  navigateToMyAnswers() {
    wx.navigateTo({
      url: '/pages/user/answers'
    });
  },

  navigateToMyVotes() {
    wx.navigateTo({
      url: '/pages/user/votes'
    });
  },

  navigateToAbout() {
    wx.navigateTo({
      url: '/pages/about/about'
    });
  },

  logout() {
    wx.removeStorageSync('userInfo');
    wx.removeStorageSync('tokens');
    wx.reLaunch({
      url: '/pages/index/index'
    });
  }
});
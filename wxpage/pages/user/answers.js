import { getUserAnswers } from '../../utils/request';

Page({
  data: {
    answers: [],
    isLoading: true,
    page: 1,
    pageSize: 10,
    hasMore: true,
    isRefreshing: false
  },

  onLoad() {
    this.loadAnswers();
  },

  onPullDownRefresh() {
    this.setData({
      page: 1,
      hasMore: true,
      isRefreshing: true
    });
    this.loadAnswers(true);
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.isLoading) {
      this.setData({
        page: this.data.page + 1
      });
      this.loadAnswers();
    }
  },

  loadAnswers(isRefresh = false) {
    const userInfo = wx.getStorageSync('userInfo');
    if (!userInfo) {
      wx.redirectTo({
        url: '/pages/login/login'
      });
      return;
    }

    this.setData({ isLoading: true });

    getUserAnswers({
      author: userInfo.id,
      ordering: '-created_at',
      page: this.data.page,
      page_size: this.data.pageSize
    }).then(res => {
      const answers = res.results || res;
      this.setData({
        answers: isRefresh ? answers : [...this.data.answers, ...answers],
        hasMore: answers.length >= this.data.pageSize,
        isLoading: false,
        isRefreshing: false
      });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
    }).catch(err => {
      this.setData({
        isLoading: false,
        isRefreshing: false
      });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
      wx.showToast({
        title: '没有更多了',
        icon: 'none'
      });
    });
  },

  navigateToQuestion(e) {
    const questionId = e.currentTarget.dataset.questionId;
    wx.navigateTo({
      url: `/pages/question/question?id=${questionId}`
    });
  }
});
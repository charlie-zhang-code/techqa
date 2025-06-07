import { getQuestions } from '../../utils/request';

Page({
  data: {
    questions: [],
    isLoading: true,
    page: 1,
    pageSize: 10,
    hasMore: true,
    isRefreshing: false
  },

  onLoad() {
    this.loadQuestions();
  },

  onPullDownRefresh() {
    this.setData({
      page: 1,
      hasMore: true,
      isRefreshing: true
    });
    this.loadQuestions(true);
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.isLoading) {
      this.setData({
        page: this.data.page + 1
      });
      this.loadQuestions();
    }
  },

  loadQuestions(isRefresh = false) {
    const userInfo = wx.getStorageSync('userInfo');
    if (!userInfo) {
      wx.redirectTo({
        url: '/pages/login/login'
      });
      return;
    }

    this.setData({ isLoading: true });

    getQuestions({
      author: userInfo.id,
      ordering: '-created_at',
      page: this.data.page,
      page_size: this.data.pageSize
    }).then(res => {
      const questions = res.results || res;
      this.setData({
        questions: isRefresh ? questions : [...this.data.questions, ...questions],
        hasMore: questions.length >= this.data.pageSize,
        isLoading: false,
        isRefreshing: false
      });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
    }).catch(err => {
      console.error('加载提问失败:', err);
      this.setData({
        isLoading: false,
        isRefreshing: false
      });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    });
  },

  navigateToQuestion(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/question/question?id=${id}`
    });
  }
});
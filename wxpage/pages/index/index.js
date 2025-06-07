import { getQuestions, getBanners, getPopularTags } from '../../utils/request';

Page({
  data: {
    banners: [],
    questions: [],
    popularTags: [],
    isLoading: true,
    page: 1,
    pageSize: 10,
    hasMore: true,
    isFetching: false,  // 请求锁
    error: null        // 错误信息
  },

  onLoad() {
    this.loadData();
  },

  onPullDownRefresh() {
    this.setData({
      page: 1,
      hasMore: true,
      error: null
    });
    this.loadData(true);
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.isLoading) {
      this.loadMoreData();
    }
  },

  loadData(isRefresh = false) {
    const oldQuestions = this.data.questions;
    this.setData({ 
      isLoading: true,
      page: isRefresh ? 1 : this.data.page,
      hasMore: true,
      error: null
    });
    
    Promise.all([
      getBanners(),
      getQuestions({ ordering: '-created_at', page: this.data.page, page_size: this.data.pageSize }),
      getPopularTags()
    ]).then(([banners, questions, tags]) => {
      this.setData({
        banners: banners.results || banners,
        questions: questions.results || questions,
        popularTags: tags,
        isLoading: false
      });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
    }).catch(err => {
      console.error('加载数据失败:', err);
      this.setData({ 
        isLoading: false,
        error: '加载失败，请重试'
      });
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
    });
  },

  loadMoreData() {
    if (!this.data.hasMore || this.data.isFetching) return;
    
    this.setData({ 
      isLoading: true,
      isFetching: true
    });
    
    const nextPage = this.data.page + 1;
    
    getQuestions({ ordering: '-created_at', page: nextPage, page_size: this.data.pageSize })
      .then(res => {
        const newQuestions = res.results || [];
        this.setData({
          questions: [...this.data.questions, ...newQuestions],
          page: nextPage,
          hasMore: newQuestions.length >= this.data.pageSize,
          isLoading: false,
          isFetching: false
        });
      })
      .catch(err => {
        this.setData({ 
          isLoading: false,
          isFetching: false,
          error: '没有更多了'
        });
        wx.showToast({
          title: '没有更多了',
          icon: 'none'
        });
      });
  },

  navigateToSearch() {
    wx.navigateTo({
      url: '/pages/search/search'
    });
  },

  navigateToQuestion(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/question/question?id=${id}`
    });
  },

  navigateToTag(e) {
    const name = e.currentTarget.dataset.name;
    wx.navigateTo({
      url: `/pages/search/search?tag=${name}`
    });
  },

  onAskTap(e) {
    // wx.navigateTo({
    //   url: `/pages/ask/ask`
    // });
  }
});
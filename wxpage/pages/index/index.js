// import { getQuestions, getBanners, getPopularTags, getHotQuestions } from '../../utils/request';

// Page({
//   data: {
//     banners: [],
//     questions: [],
//     popularTags: [],
//     isLoading: true,
//     page: 1,
//     pageSize: 10,
//     hasMore: true,
//     hotQuestions: [],
//     isFetching: false,  // 请求锁
//     error: null        // 错误信息
//   },

//   onLoad() {
//     this.loadData();
//   },

//   onPullDownRefresh() {
//     this.setData({
//       page: 1,
//       hasMore: true,
//       error: null
//     });
//     this.loadData(true);
//   },

//   onReachBottom() {
//     if (this.data.hasMore && !this.data.isLoading) {
//       this.loadMoreData();
//     }
//   },

//   loadData(isRefresh = false) {
//     const oldQuestions = this.data.questions;
//     this.setData({
//       isLoading: true,
//       page: isRefresh ? 1 : this.data.page,
//       hasMore: true,
//       error: null
//     });

//     Promise.all([
//       getBanners(),
//       getQuestions({ ordering: '-created_at', page: this.data.page, page_size: this.data.pageSize }),
//       getPopularTags()
//     ]).then(([banners, questions, tags]) => {
//       this.setData({
//         banners: banners.results || banners,
//         questions: questions.results || questions,
//         popularTags: tags,
//         isLoading: false
//       });
//       if (isRefresh) {
//         wx.stopPullDownRefresh();
//       }
//     }).catch(err => {
//       console.error('加载数据失败:', err);
//       this.setData({
//         isLoading: false,
//         error: '加载失败，请重试'
//       });
//       wx.showToast({
//         title: '加载失败',
//         icon: 'none'
//       });
//       if (isRefresh) {
//         wx.stopPullDownRefresh();
//       }
//     });

//      getHotQuestions().then(res => {
//       this.setData({ hotQuestions: res });
//     });
//   },

//   loadMoreData() {
//     if (!this.data.hasMore || this.data.isFetching) return;

//     this.setData({
//       isLoading: true,
//       isFetching: true
//     });

//     const nextPage = this.data.page + 1;

//     getQuestions({ ordering: '-created_at', page: nextPage, page_size: this.data.pageSize })
//       .then(res => {
//         const newQuestions = res.results || [];
//         this.setData({
//           questions: [...this.data.questions, ...newQuestions],
//           page: nextPage,
//           hasMore: newQuestions.length >= this.data.pageSize,
//           isLoading: false,
//           isFetching: false
//         });
//       })
//       .catch(err => {
//         this.setData({
//           isLoading: false,
//           isFetching: false,
//           error: '没有更多了'
//         });
//         wx.showToast({
//           title: '没有更多了',
//           icon: 'none'
//         });
//       });
//   },

//   navigateToSearch() {
//     wx.navigateTo({
//       url: '/pages/search/search'
//     });
//   },

//   navigateToQuestion(e) {
//     const id = e.currentTarget.dataset.id;
//     wx.navigateTo({
//       url: `/pages/question/question?id=${id}`
//     });
//   },

//   navigateToTag(e) {
//     const name = e.currentTarget.dataset.name;
//     wx.navigateTo({
//       url: `/pages/search/search?tag=${name}`
//     });
//   },

//   onAskTap(e) {
//     // wx.navigateTo({
//     //   url: `/pages/ask/ask`
//     // });
//   }
// });






import { getQuestions, getBanners, getPopularTags, getHotQuestions } from '../../utils/request';

Page({
  data: {
    banners: [],
    questions: [], // 最新问题列表
    popularTags: [],
    isLoading: true,
    page: 1,
    pageSize: 10,
    hasMore: true,
    hotQuestions: [], // 热门问题列表
    hotQuestionsLoading: false, // 热门问题加载状态
    activeTab: 'latest', // 当前选中的标签页，默认为最新提问
    isFetching: false,  // 请求锁
    error: null        // 错误信息
  },

  onLoad() {
    this.loadData();
  },

  onPullDownRefresh() {
    if (this.data.activeTab === 'latest') {
      this.setData({
        page: 1,
        hasMore: true,
        error: null
      });
      this.loadData(true);
    } else {
      // 刷新热门问题
      this.loadHotQuestions(true);
    }
  },

  onReachBottom() {
    if (this.data.activeTab === 'latest' && this.data.hasMore && !this.data.isLoading) {
      this.loadMoreData();
    }
    // 热门问题不分页，所以不需要处理
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

    // 加载热门问题（不分页）
    this.loadHotQuestions();
  },

  // 新增方法：加载热门问题
  loadHotQuestions(isRefresh = false) {
    if (isRefresh) {
      this.setData({
        hotQuestionsLoading: true
      });
    }

    getHotQuestions().then(res => {
      this.setData({ 
        hotQuestions: res,
        hotQuestionsLoading: false
      });
    }).catch(err => {
      console.error('加载热门问题失败:', err);
      this.setData({
        hotQuestionsLoading: false,
        error: '加载热门问题失败'
      });
      wx.showToast({
        title: '加载热门问题失败',
        icon: 'none'
      });
    });
  },

  // 修改加载更多数据的方法，只针对最新问题
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

  // 新增方法：切换Tab
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    if (this.data.activeTab === tab) return; // 如果已经是当前Tab，不做任何操作
    
    this.setData({
      activeTab: tab
    });
    
    // 如果切换到热门提问且还没有加载过数据，则加载热门问题
    if (tab === 'hot' && this.data.hotQuestions.length === 0) {
      this.loadHotQuestions();
    }
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
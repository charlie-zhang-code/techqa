import { getMyVote } from '../../utils/request';

Page({
  data: {
    allVotes: [], // 存储所有投票数据
    filteredVotes: [], // 存储过滤后的数据
    isLoading: true,
    activeTab: 'all' // 'all', 'up', 'down'
  },

  onLoad() {
    this.loadVotes();
  },

  onPullDownRefresh() {
    this.loadVotes(true);
  },

  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({
      activeTab: tab
    }, () => {
      this.filterVotes(); // 切换tab后重新过滤数据
    });
  },

  loadVotes(isRefresh = false) {
    this.setData({ isLoading: true });

    getMyVote().then(res => {
      this.setData({
        allVotes: res,
        isLoading: false
      }, () => {
        this.filterVotes(); // 加载数据后立即过滤
      });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
    }).catch(err => {
      this.setData({ isLoading: false });
      if (isRefresh) {
        wx.stopPullDownRefresh();
      }
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    });
  },

  // 新增的过滤方法
  filterVotes() {
    const { allVotes, activeTab } = this.data;
    let filtered = [];
    
    if (activeTab === 'all') {
      filtered = allVotes;
    } else {
      filtered = allVotes.filter(vote => vote.vote_type === activeTab);
    }
    
    this.setData({
      filteredVotes: filtered
    });
  },

  navigateToTarget(e) {
    const vote = e.currentTarget.dataset.vote;
    if (vote.question) {
      wx.navigateTo({
        url: `/pages/question/question?id=${vote.question}`
      });
    } else if (vote.answer && vote.answer.question) {
      wx.navigateTo({
        url: `/pages/question/question?id=${vote.answer.question}`
      });
    }
  }
});
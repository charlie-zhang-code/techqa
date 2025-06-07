// pages/search/search.js
import { getQuestions, getTags } from '../../utils/request';

Page({
    data: {
        searchType: 'question', // 'question' 或 'tag'
        searchText: '',
        questions: [],
        tags: [],
        isLoading: false,
        activeTab: 'question', // 'question' 或 'tag'
        selectedTag: null
    },

    onLoad(options) {
        // 从首页点击标签跳转过来会带tag参数
        if (options.tag) {
            this.setData({
                activeTab: 'tag',
                selectedTag: options.tag,
                searchText: options.tag
            }, () => {
                this.searchByTag(options.tag);
            });
        }
    },

    onSearchInput(e) {
        this.setData({ searchText: e.detail.value });
    },

    switchTab(e) {
        const tab = e.currentTarget.dataset.tab;
        this.setData({
            activeTab: tab,
            questions: [],
            tags: []
        });
    },

    search() {
        const { searchText, activeTab } = this.data;
        if (!searchText.trim()) {
            wx.showToast({
                title: '请输入搜索内容',
                icon: 'none'
            });
            return;
        }

        if (activeTab === 'question') {
            this.searchQuestions(searchText);
        } else {
            this.searchTags(searchText);
        }
    },

    searchQuestions(keyword) {
        this.setData({ isLoading: true });
        getQuestions({ search: keyword, ordering: '-created_at' })
            .then(res => {
                this.setData({
                    questions: res.results || res,
                    isLoading: false
                });
            })
            .catch(err => {
                console.error('搜索问题失败:', err);
                wx.showToast({
                    title: '搜索失败',
                    icon: 'none'
                });
                this.setData({ isLoading: false });
            });
    },

    searchTags(keyword) {
        this.setData({ isLoading: true });
        getTags({ search: keyword })
            .then(res => {
                this.setData({
                    tags: res.results || res,
                    isLoading: false
                });
            })
            .catch(err => {
                console.error('搜索标签失败:', err);
                wx.showToast({
                    title: '搜索失败',
                    icon: 'none'
                });
                this.setData({ isLoading: false });
            });
    },

    searchByTag(tagName) {
        this.setData({ isLoading: true });
        getQuestions({ tag_name: tagName, ordering: '-created_at' })
            .then(res => {
                this.setData({
                    questions: res.results || res,
                    isLoading: false
                });
            })
            .catch(err => {
                console.error('按标签搜索问题失败:', err);
                wx.showToast({
                    title: '搜索失败',
                    icon: 'none'
                });
                this.setData({ isLoading: false });
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
        this.setData({
            selectedTag: name,
            searchText: name
        }, () => {
            this.searchByTag(name);
        });
    }
});
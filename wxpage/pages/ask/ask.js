// pages/ask/ask.js
import { getTags, createQuestion } from '../../utils/request';

Page({
    data: {
        title: '',
        content: '',
        selectedTags: [],
        allTags: [],
        newTagName: '',
        isAnonymous: false,
        isSubmitting: false
    },

    onLoad() {
        this.loadAllTags();
    },

    loadAllTags() {
        getTags().then(res => {
            this.setData({
                allTags: res.results || res
            });
        }).catch(err => {
            console.error('加载标签失败:', err);
            wx.showToast({
                title: '加载标签失败',
                icon: 'none'
            });
        });
    },

    onTitleInput(e) {
        this.setData({ title: e.detail.value });
    },

    onContentInput(e) {
        this.setData({ content: e.detail.value });
    },

    onTagSelect(e) {
        const index = e.detail.value;
        const selectedTag = this.data.allTags[index];

        // 检查是否已选择
        const isSelected = this.data.selectedTags.some(tag => tag.id === selectedTag.id);
        if (!isSelected) {
            this.setData({
                selectedTags: [...this.data.selectedTags, selectedTag]
            });
        }
    },

    onNewTagInput(e) {
        this.setData({ newTagName: e.detail.value });
    },

    addNewTag() {
        const newTagName = this.data.newTagName.trim();
        if (!newTagName) return;

        // 检查是否已存在
        const existingTag = this.data.allTags.find(tag =>
            tag.name.toLowerCase() === newTagName.toLowerCase()
        );

        if (existingTag) {
            // 已存在，直接添加
            const isSelected = this.data.selectedTags.some(tag => tag.id === existingTag.id);
            if (!isSelected) {
                this.setData({
                    selectedTags: [...this.data.selectedTags, existingTag],
                    newTagName: ''
                });
            }
        } else {
            // 新标签，添加到选择列表
            const newTag = {
                id: `new_${Date.now()}`,
                name: newTagName
            };
            this.setData({
                selectedTags: [...this.data.selectedTags, newTag],
                newTagName: ''
            });
        }
    },

    removeTag(e) {
        const tagId = e.currentTarget.dataset.id;
        this.setData({
            selectedTags: this.data.selectedTags.filter(tag => tag.id !== tagId)
        });
    },

    onAnonymousChange(e) {
        this.setData({ isAnonymous: e.detail.value });
    },

    submitQuestion() {
        if (!((this.data.title != '') && (this.data.content != ''))) {
            wx.showToast({
                title: '请填写标题和内容',
                icon: 'none'
            });
            return;
        }

        this.setData({ isSubmitting: true });

        const tagNames = this.data.selectedTags.map(tag => tag.name);
        const data = {
            title: this.data.title,
            content: this.data.content,
            tag_names: tagNames,
            is_anonymous: this.data.isAnonymous
        };

        createQuestion(data)
            .then(res => {
                wx.showToast({
                    title: '提问成功',
                    icon: 'success'
                });

                // 返回首页并刷新
                setTimeout(() => {
                    wx.switchTab({
                        url: '/pages/index/index'
                    });
                }, 1500);

                // 清除数据
                this.setData({
                    title: '',
                    content: '',
                    selectedTags: [],
                    newTagName: ''
                })
            })
            .catch(err => {
                console.error('提交问题失败:', err);
                wx.showToast({
                    title: '提问失败',
                    icon: 'none'
                });
            })
            .finally(() => {
                this.setData({ isSubmitting: false });
            });
    },

    get canSubmit() {
        return (this.data.title != '') && (this.data.content != '');
    }
});
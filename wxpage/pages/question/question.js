import {
    getQuestionDetail,
    getAnswers,
    getComments,
    createAnswer,
    createComment,
    voteAnswer,
    acceptAnswer,
    incrementViews,
    voteQuestion
} from '../../utils/request';

Page({
    data: {
        question: null,
        answers: [],
        comments: [],
        newAnswerContent: '',
        newCommentContent: '',
        loading: true,
        isOwner: false,
        activeTab: 'answers', // 'answers' or 'comments'
        replyTo: null, // 回复的评论ID
        currentPage: 1,
        pageSize: 10,
        hasMore: true
    },
    
    onLoad(options) {
        const questionId = options.id;
        this.setData({ questionId });
        this.loadQuestionDetail(questionId);
        this.loadAnswers(questionId);
        this.loadComments(questionId);

        // 增加浏览量
        incrementViews(questionId);
    },

    loadQuestionDetail(questionId) {
        getQuestionDetail(questionId).then(res => {
            const userInfo = wx.getStorageSync('userInfo');
            const isOwner = userInfo && userInfo.id === res.author.id;

            this.setData({
                question: res,
                isOwner,
                loading: false
            });
        }).catch(err => {
            console.error('加载问题详情失败:', err);
            wx.showToast({
                title: '加载失败',
                icon: 'none'
            });
            this.setData({ loading: false });
        });
    },

    loadAnswers(questionId) {
        getAnswers(questionId, {
            page: this.data.currentPage,
            page_size: this.data.pageSize
        }).then(res => {
            const answers = res.results || res;
            this.setData({
                answers,
                hasMore: answers.length >= this.data.pageSize
            });
        }).catch(err => {
            console.error('加载回答失败:', err);
            wx.showToast({
                title: '加载回答失败',
                icon: 'none'
            });
        });
    },

    loadComments(questionId) {
        getComments(questionId).then(res => {
            const comments = res.results || res;
            this.setData({ comments });
        }).catch(err => {
            console.error('加载评论失败:', err);
            wx.showToast({
                title: '加载评论失败',
                icon: 'none'
            });
        });
    },

    onReachBottom() {
        if (this.data.hasMore && this.data.activeTab === 'answers') {
            this.setData({
                currentPage: this.data.currentPage + 1
            });
            this.loadAnswers(this.data.questionId);
        }
    },

    switchTab(e) {
        const tab = e.currentTarget.dataset.tab;
        this.setData({ activeTab: tab });
    },

    handleAnswerInput(e) {
        this.setData({ newAnswerContent: e.detail.value });
    },

    handleCommentInput(e) {
        this.setData({ newCommentContent: e.detail.value });
    },

    submitAnswer() {
        if (!this.data.newAnswerContent.trim()) {
            wx.showToast({
                title: '请输入回答内容',
                icon: 'none'
            });
            return;
        }

        const data = {
            content: this.data.newAnswerContent,
            question: this.data.questionId
        };

        createAnswer(data).then(res => {
            wx.showToast({
                title: '回答成功',
                icon: 'success'
            });
            this.setData({ newAnswerContent: '' });
            this.loadAnswers(this.data.questionId);
        }).catch(err => {
            console.error('提交回答失败:', err);
            wx.showToast({
                title: '回答失败',
                icon: 'none'
            });
        });
    },

    submitComment() {
        if (!this.data.newCommentContent.trim()) {
            wx.showToast({
                title: '请输入评论内容',
                icon: 'none'
            });
            return;
        }

        const data = {
            content: this.data.newCommentContent,
            question: this.data.questionId,
            reply_to: this.data.replyTo
        };

        createComment(data).then(res => {
            wx.showToast({
                title: '评论成功',
                icon: 'success'
            });
            this.setData({
                newCommentContent: '',
                replyTo: null
            });
            this.loadComments(this.data.questionId);
        }).catch(err => {
            console.error('提交评论失败:', err);
            wx.showToast({
                title: '评论失败',
                icon: 'none'
            });
        });
    },

    voteQuestion(e) {
        const questionId = e.currentTarget.dataset.id;
        const voteType = e.currentTarget.dataset.type;

        voteQuestion(questionId, voteType).then(res => {
            // 重新加载问题详情以更新投票状态
            this.loadQuestionDetail(this.data.questionId);
            wx.showToast({
                title: '投票成功',
                icon: 'success'
            });
        }).catch(err => {
            console.error('投票失败:', err);
            wx.showToast({
                title: '投票失败',
                icon: 'none'
            });
        });
    },

    voteAnswer(e) {
        const answerId = e.currentTarget.dataset.id;
        const voteType = e.currentTarget.dataset.type;

        voteAnswer(answerId, voteType).then(res => {
            this.loadAnswers(this.data.questionId);
        }).catch(err => {
            console.error('投票失败:', err);
            wx.showToast({
                title: '投票失败',
                icon: 'none'
            });
        });
    },

    acceptAnswer(e) {
        const answerId = e.currentTarget.dataset.id;
        const isAccepted = e.currentTarget.dataset.accept === 'true';

        acceptAnswer(answerId, isAccepted).then(res => {
            this.loadAnswers(this.data.questionId);
            this.loadQuestionDetail(this.data.questionId);
            wx.showToast({
                title: isAccepted ? '已采纳回答' : '已取消采纳',
                icon: 'success'
            });
        }).catch(err => {
            console.error('采纳回答失败:', err);
            wx.showToast({
                title: '操作失败',
                icon: 'none'
            });
        });
    },

    replyComment(e) {
        const commentId = e.currentTarget.dataset.id;
        const username = e.currentTarget.dataset.username;

        this.setData({
            replyTo: commentId,
            newCommentContent: `@${username} `
        });
    }
});
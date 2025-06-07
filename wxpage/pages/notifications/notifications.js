// pages/notifications/notifications.js
import { getNotifications, getUnreadCount, markAllAsRead } from '../../utils/request';
Page({
    data: {
        notifications: [],
        unreadCount: 0,
        isLoading: true,
        isMarkingAll: false
    },

    onLoad() {
        this.loadNotifications();
    },

    onShow() {
        this.loadUnreadCount();
    },

    onPullDownRefresh() {
        this.loadNotifications(true);
    },

    getNotificationTypeText(type) {
        const types = {
            'question_answered': '问题被回答',
            'answer_commented': '回答被评论',
            'answer_accepted': '回答被采纳',
            'mentioned': '被提及',
            'question_commented': '问题被评论',
            'comment_replied': '评论被回复'
        };
        return types[type];
    },
    getNotificationContent(notification) {
        const { notification_type, question, answer } = notification;

        switch (notification_type) {
            case 'question_answered':
                return `回答了你的问题: ${question.title}`;
            case 'answer_commented':
                return `评论了你的回答`;
            case 'answer_accepted':
                return `采纳了你的回答`;
            case 'question_commented':
                return `评论了你的问题: ${question.title}`;
            case 'comment_replied':
                return `回复了你的评论`;
            case 'mentioned':
                return `在${question ? '问题' : '回答'}中提到了你`;
            default:
                return '';
        }
    },
    loadNotifications(isRefresh = false) {
        this.setData({ isLoading: true });

        getNotifications()
            .then(res => {
                const notifications = (res.results || res).map(item => {
                    return {
                        ...item,
                        typeText: this.getNotificationTypeText(item.notification_type),
                        notificationText: this.getNotificationContent(item)
                    };
                });
                this.setData({
                    notifications: notifications,
                    isLoading: false
                });
                if (isRefresh) {
                    wx.stopPullDownRefresh();
                }
                this.loadUnreadCount();
            })
            .catch(err => {
                console.error('加载通知失败:', err);
                wx.showToast({
                    title: '加载通知失败',
                    icon: 'none'
                });
                this.setData({ isLoading: false });
                if (isRefresh) {
                    wx.stopPullDownRefresh();
                }
            });
    },

    loadUnreadCount() {
        getUnreadCount()
            .then(res => {
                this.setData({ unreadCount: res.count || 0 });
            })
            .catch(err => {
                console.error('获取未读数量失败:', err);
            });
    },

    markAllAsRead() {
        this.setData({ isMarkingAll: true });

        markAllAsRead()
            .then(res => {
                wx.showToast({
                    title: '全部标记为已读',
                    icon: 'success'
                });
                this.loadNotifications();
                this.setData({ unreadCount: 0 });
            })
            .catch(err => {
                console.error('标记全部已读失败:', err);
                wx.showToast({
                    title: '操作失败',
                    icon: 'none'
                });
            })
            .finally(() => {
                this.setData({ isMarkingAll: false });
            });
    },

    navigateToTarget(e) {
        const notification = e.currentTarget.dataset.notification;
        const { notification_type, question, answer, comment } = notification;

        // 根据通知类型决定跳转目标
        let url = '';
        if (question) {
            url = `/pages/question/question?id=${question.id}`;
        } else if (answer && answer.question) {
            url = `/pages/question/question?id=${answer.question}`;
        }

        if (url) {
            wx.navigateTo({
                url: url
            });
        }
    }
});
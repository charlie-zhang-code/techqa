Page({
    data: {
      version: '1.0.0',
      features: [
        '技术问答交流平台',
        '支持提问、回答、评论',
        '投票赞同/反对机制',
        '标签分类系统',
        '微信小程序便捷访问',
        '响应式设计，多端适配'
      ],
      backendInfo: {
        framework: 'Django 4.x + Django Rest Framework',
        database: 'MySQL/PostgreSQL',
        authentication: 'JWT Token',
        cache: 'Redis'
      },
      contact: {
        email: 'support@techqa.com',
        wechat: 'TechQA_Official'
      },
      updateLogs: [
        {
          version: '1.0.0',
          date: '2023-10-15',
          items: [
            '初始版本发布',
            '基础问答功能实现',
            '微信登录集成'
          ]
        }
      ]
    },
  
    onLoad() {
      // 可以在这里添加获取最新版本信息的逻辑
    },
  
    copyContact(e) {
      const type = e.currentTarget.dataset.type;
      const content = this.data.contact[type];
      
      wx.setClipboardData({
        data: content,
        success: () => {
          wx.showToast({
            title: '已复制',
            icon: 'success'
          });
        }
      });
    }
  });
// utils/request.js
const BASE_URL = 'http://localhost:8000/api/';

const request = (url, method, data = {}, isAuth = true) => {
  return new Promise((resolve, reject) => {
    const header = {
      'Content-Type': 'application/json'
    };
    
    if (isAuth) {
      const tokens = wx.getStorageSync('tokens');
      if (tokens && tokens.access) {
        header['Authorization'] = `Bearer ${tokens.access}`;
      }
    }
    
    wx.request({
      url: BASE_URL + url,
      method: method,
      data: data,
      header: header,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(res.data);
        }
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
};

// 用户相关API
export const wxLogin = (code) => request('users/wx_login/', 'POST', { code }, false);
export const getUserInfo = (userId) => request(`users/${userId}/`, 'GET');
export const updateUserInfo = (userId, data) => request(`users/${userId}/`, 'PATCH', data);
export const followUser = (userId, action) => request(`users/${userId}/follow/`, 'POST', { action });

// 问题相关API
// export const getQuestions = (params) => request('questions/', 'GET', params);
export const getQuestions = (params) => {
    // 如果传入了tag_name参数，转换为tags__name
    if (params.tag_name) {
      params.tags__name = params.tag_name;
      delete params.tag_name;
    }
    return request('questions/', 'GET', params);
  };
export const getQuestionDetail = (questionId) => request(`questions/${questionId}/`, 'GET');
export const createQuestion = (data) => request('questions/', 'POST', data);
export const updateQuestion = (questionId, data) => request(`questions/${questionId}/`, 'PATCH', data);
export const voteQuestion = (questionId, voteType) => request(`questions/${questionId}/vote/`, 'POST', { vote_type: voteType });
export const incrementViews = (questionId) => request(`questions/${questionId}/increment_views/`, 'POST');

// 投票相关
export const getMyVote = () => request(`votes/my_votes/`, 'GET');

// 回答相关API
export const getAnswers = (questionId) => request(`questions/${questionId}/answers/`, 'GET');
export const getUserAnswers = (params) => request('answers/', 'GET', params);
export const createAnswer = (data) => request('answers/', 'POST', data);
export const updateAnswer = (answerId, data) => request(`answers/${answerId}/`, 'PATCH', data);
export const voteAnswer = (answerId, voteType) => request(`answers/${answerId}/vote/`, 'POST', { vote_type: voteType });
export const acceptAnswer = (answerId, isAccepted) => request(`answers/${answerId}/accept/`, 'POST', { is_accepted: isAccepted });

// 评论相关API
export const getComments = (questionId) => request(`questions/${questionId}/comments/`, 'GET');
export const createComment = (data) => request('comments/', 'POST', data);

// 标签相关API
export const getTags = () => request('tags/', 'GET');
export const getPopularTags = () => request('tags/popular/', 'GET');
export const followTag = (tagId, action) => request(`tags/${tagId}/follow/`, 'POST', { action });

// 通知相关API
export const getNotifications = () => request('notifications/', 'GET');
export const getUnreadCount = () => request('notifications/unread_count/', 'GET');
export const markAllAsRead = () => request('notifications/mark_all_as_read/', 'POST');

// 轮播图API
export const getBanners = () => request('banners/', 'GET');

export default {
  wxLogin,
  getUserInfo,
  updateUserInfo,
  followUser,
  getQuestions,
  getQuestionDetail,
  createQuestion,
  updateQuestion,
  voteQuestion,
  incrementViews,
  getAnswers,
  createAnswer,
  updateAnswer,
  voteAnswer,
  acceptAnswer,
  getComments,
  createComment,
  getTags,
  getPopularTags,
  followTag,
  getNotifications,
  getUnreadCount,
  markAllAsRead,
  getBanners,
  getMyVote,
  getUserAnswers
};
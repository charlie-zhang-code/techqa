# qa/services/wx_auth.py
import requests
from django.conf import settings


class WxAuthService:
    def __init__(self):
        self.app_id = settings.WX_APP_ID
        self.app_secret = settings.WX_APP_SECRET
        self.login_url = settings.WX_LOGIN_URL

    def get_wx_user_info(self, code):
        params = {
            'appid': self.app_id,
            'secret': self.app_secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }

        try:
            response = requests.get(self.login_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
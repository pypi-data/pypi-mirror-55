# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class Security(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(Security, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # imgSecCheck, Refer: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.imgSecCheck.html
        self.WECHAT_IMG_SEC_CHECK = self.API_DOMAIN + '/wxa/img_sec_check?access_token={access_token}'
        # msgSecCheck, Refer: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.msgSecCheck.html
        self.WECHAT_MSG_SEC_CHECK = self.API_DOMAIN + '/wxa/msg_sec_check?access_token={access_token}'
        # mediaCheckAsync, Refer: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.mediaCheckAsync.html
        self.WECHAT_MEDIA_CHECK_ASYNC = self.API_DOMAIN + '/wxa/media_check_async?access_token={access_token}'

    def img_sec_check(self, media_file=None, media_file_path=None, appid=None, secret=None, token=None, storage=None, res_bool_val=False):
        res = self.post(
            self.WECHAT_IMG_SEC_CHECK.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            files={
                'media': media_file or open(media_file_path, 'rb'),
            },
        )
        return res.get('errcode') == 0 if res_bool_val else res

    def msg_sec_check(self, content, appid=None, secret=None, token=None, storage=None, res_bool_val=False):
        res = self.post(
            self.WECHAT_MSG_SEC_CHECK.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'content': content,
            },
        )
        return res.get('errcode') == 0 if res_bool_val else res

    def media_check_async(self, media_url=None, media_type=None, appid=None, secret=None, token=None, storage=None, res_bool_val=False):
        res = self.post(
            self.WECHAT_MEDIA_CHECK_ASYNC.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data={
                'media_url': media_url,
                'media_type': media_type,
            },
        )
        return res.get('errcode') == 0 if res_bool_val else res

    def audio_check_async(self, audio_url=None, media_url=None, appid=None, secret=None, token=None, storage=None, res_bool_val=False):
        return self.media_check_async(media_url=audio_url or media_url, media_type=1, appid=appid, secret=secret, token=token, storage=storage, res_bool_val=res_bool_val)

    def img_check_async(self, img_url=None, media_url=None, appid=None, secret=None, token=None, storage=None, res_bool_val=False):
        return self.media_check_async(media_url=img_url or media_url, media_type=2, appid=appid, secret=secret, token=token, storage=storage, res_bool_val=res_bool_val)


security = Security()
img_sec_check = security.img_sec_check
msg_sec_check = security.msg_sec_check
media_check_async = security.media_check_async
audio_check_async = security.audio_check_async
img_check_async = security.img_check_async

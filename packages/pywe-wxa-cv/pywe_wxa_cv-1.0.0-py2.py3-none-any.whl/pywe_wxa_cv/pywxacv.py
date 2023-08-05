# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class CV(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(CV, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # aiCrop, Refer: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/img/img.aiCrop.html
        self.WECHAT_CV_AICROP = self.API_DOMAIN + '/cv/img/aicrop?img_url={img_url}&access_token={access_token}'
        # scanQRCode, Refer: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/img/img.scanQRCode.html
        self.WECHAT_CV_QRCODE = self.API_DOMAIN + '/cv/img/qrcode?img_url={img_url}&access_token={access_token}'
        # superresolution, Refer: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/img/img.superresolution.html
        self.WECHAT_CV_SUPERRESOLUTION = self.API_DOMAIN + '/cv/img/superresolution?img_url={img_url}&access_token={access_token}'

    def aicrop(self, img_url=None, img_file=None, img_file_path=None, ratios=None, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CV_AICROP.format(img_url=img_url, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            files={
                'img': img_file or open(img_file_path, 'rb'),
                'ratios': ratios,
            },
        )

    def qrcode(self, img_url=None, img_file=None, img_file_path=None, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CV_QRCODE.format(img_url=img_url, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            files={
                'img': img_file or open(img_file_path, 'rb'),
            },
        )

    def superresolution(self, img_url=None, img_file=None, img_file_path=None, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CV_SUPERRESOLUTION.format(img_url=img_url, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            files={
                'img': img_file or open(img_file_path, 'rb'),
            },
        )


cv = CV()
cv_aicrop = cv.aicrop
cv_qrcode = cv.qrcode
cv_superresolution = cv.superresolution

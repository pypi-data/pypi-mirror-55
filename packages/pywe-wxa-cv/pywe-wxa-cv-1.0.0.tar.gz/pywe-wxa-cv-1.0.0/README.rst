===========
pywe-wxa-cv
===========

Wechat MiniProgram CV Module for Python.

Sandbox
=======

* https://developers.weixin.qq.com/sandbox

Installation
============

::

    pip install pywe-wxa-cv


Usage
=====

::

    from pywe_wxa_cv import CV, cv_aicrop, cv_qrcode, cv_superresolution


Method
======

::

    class CV(BaseToken):
        def __init__(self, appid=None, secret=None, token=None, storage=None):
            super(CV, self).__init__(appid=appid, secret=secret, token=token, storage=storage)

    def aicrop(self, img_url=None, img_file=None, img_file_path=None, ratios=None, appid=None, secret=None, token=None, storage=None):

    def qrcode(self, img_url=None, img_file=None, img_file_path=None, appid=None, secret=None, token=None, storage=None):

    def superresolution(self, img_url=None, img_file=None, img_file_path=None, appid=None, secret=None, token=None, storage=None):


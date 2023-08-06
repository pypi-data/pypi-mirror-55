#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2019-11-07 12:59:23
'''
from .application import Blueprint
from .basehandler import BaseHandler
bp = Blueprint('wechat')


@bp.route('/wechat/callback')
class WechatCallback(BaseHandler):
    '''
    每日神贴: wxc3669cedfcbe12ac, d6ea06c50a0181bc50264af4dcdb5550
    '''

    def get(self):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid': self.app.appid,
            'secret': self.app.appsecret,
            'code': self.args.code,
            'grant_type': 'authorization_code',
        }
        resp = await self.http.get(url, params=params)
        ret = resp.json()
        if ret.access_token:
            url = 'https://api.weixin.qq.com/sns/userinfo'
            params = {
                'access_token': ret.access_token
            }
            resp = await self.http.get(url, params)
            ret = resp.json()

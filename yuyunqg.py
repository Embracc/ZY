# -*- coding: utf-8 -*-
"""
cron: 59 59 19 * * *
new Env('雨云抢香港机');
"""
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
import logging
import json
import os

 #第四步：时间规则：0 0 23 * * ?    #每天 23 点执行一次 （可以按自己的需求，每天执行一次）

import warnings
warnings.filterwarnings('ignore')

class RainYun():

    def __init__(self, user: str, pwd: str) -> None:
        # 认证信息
        self.user = user.lower()
        self.pwd = pwd
        self.json_data = json.dumps({
            "field": self.user,
            "password": self.pwd,
        })
        self.data = {
            "item_id": 107
        }
        
        # 日志输出
        self.logger = logging.getLogger(self.user)
        formatter = logging.Formatter(datefmt='%Y/%m/%d %H:%M:%S',
                                      fmt="%(asctime)s 雨云 %(levelname)s: 用户<%(name)s> %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        # 签到结果初始化
        self.signin_result = False
        # 请求设置
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            "Origin": "https://api.rainyun.cc",
            "Referer": "https://api.rainyun.cc"
        })
        self.login_url = "https://api.v2.rainyun.cc:36688/user/login"
        self.signin_url = "https://api.v2.rainyun.cc:36688/user/reward/tasks"
        self.logout_url = "https://api.v2.rainyun.cc:36688/user/logout"
        self.query_url = "https://api.v2.rainyun.cc:36688/user/"
        self.items_url = "https://api.v2.rainyun.cc:36688/user/reward/items"
        # 忽略 .cc ssl错误
        self.session.verify = False

    def login(self) -> None:
        """登录"""
        res = self.session.post(
            url=self.login_url, headers={"Content-Type": "application/json"}, data=self.json_data)
        if res.text.find("200") > -1:
            self.logger.info("登录成功")
            csrf_token = res.cookies.get("X-CSRF-Token", "")
            self.session.headers.update({
                "X-CSRF-Token": csrf_token
            })
            self.logger.info(f"获取到的Token为: {csrf_token}")
        else:
            self.logger.error(f"登录失败，响应信息：{res.text}")

    

if __name__ == '__main__':
    accounts = [
        {
            "user": os.environ['yuyun'].split('@')[0],
            "password": os.environ['yuyun'].split('@')[1]
        }
    ]
    for acc in accounts:
        ry = RainYun(acc["user"], acc["password"])  # 实例
        ry.login()  # 登录
        ry.logout()  # 登出
        # 保存日志则打开注释 推荐文件绝对路径
        # file = "./rainyun-signin-log.json"
        # 日志最大记录数量
        # max_num = 5
        # ry.log(file, max_num)  # 保存日志

# -*- coding: utf-8 -*-
"""
cron: 0 0 23 * * ?
new Env('雨云挂机');
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
        self.logout_url = "https://api.v2.rainyun.cc:36688/user/logout"
        self.items_url = "https://api.v2.rainyun.cc:36688/user/reward/items"

        # 忽略 .cc ssl错误
        self.session.verify = False

    def login(self) -> None:
        """登录"""
        res = self.session.post(
            url=self.login_url, headers={"Content-Type": "application/json"}, data=self.json_data)
        if res.text.find("200") > -1:
            self.logger.info("登录成功")
            self.session.headers.update({
                "X-CSRF-Token": res.cookies.get("X-CSRF-Token", "")
            })
            self.token = res.cookies.get("X-CSRF-Token", "")
            self.cookies = res.cookies  # 将响应中的 Cookie 存储到 self.cookies 变量中
            self.logger.info(f"获取到的Token为: {self.token}")
            self.session.headers.update({"X-CSRF-Token": self.token})
            res = self.session.post(
            url=self.items_url, headers={"Content-Type": "application/json", "x-csrf-token": self.token, "cookie": acc.get("cookie")}, data={"item_id": 107})


            self.logger.info(f"抢了一次，响应信息：{res.text}")
        else:
            self.logger.error(f"登录失败，响应信息：{res.text}")

    def logout(self) -> None:
        res = self.session.post(url=self.logout_url)
        if res.text.find("200") > -1:
            self.logger.info('已退出登录')
        else:
            self.logger.warning(f"退出登录时出了些问题，响应信息：{res.text}")



    def log(self, log_file: str, max_num=5) -> None:
        """存储本次签到结果的日志"""
        # 北京时间
        time_string = self.signin_date.replace(tzinfo=timezone.utc).astimezone(
            timezone(timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")
        file = Path(log_file)
        record = {
            "date": time_string,
            "result": self.signin_result,
            "points": self.points
        }
        previous_records = {}
        if file.is_file():
            try:
                with open(log_file, 'r') as f:
                    previous_records = json.load(f)
                if not previous_records.get(self.user):
                    previous_records[self.user] = []
                previous_records[self.user].insert(0, record)
                previous_records[self.user] = previous_records[self.user][:max_num]
            except Exception as e:
                self.logger.error("序列化日志时出错："+repr(e))
        else:
            previous_records[self.user] = [record]
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(previous_records, f, indent=4)
        self.logger.info('日志保存成功')


if __name__ == '__main__':
    accounts = [
        {
            "user": os.environ['yuyun'].split('@')[0],
            "password": os.environ['yuyun'].split('@')[1],
            "cookie" : os.environ['yycookie']
        }
    ]
    for acc in accounts:
        ry = RainYun(acc["user"], acc["password"])  # 实例
        ry.login()  # 登录
        ry.logout()  # 登出


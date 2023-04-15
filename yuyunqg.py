# -*- coding: utf-8 -*-
"""
59 59 19 * * *
new Env('雨云抢机子');
"""
import requests
import os

# 从环境变量获取 cookie 和 token 值
cookie, token = os.environ['yycookie'].split('&')

headers = {
    "Content-Type": "application/json",
    "x-csrf-token": token,
    "cookie": cookie
}

items_url = "https://api.v2.rainyun.cc:36688/user/reward/items"

data = {"item_id": 107} #香港机
response = requests.post(url=items_url, headers=headers, json=data)
print(response.text)

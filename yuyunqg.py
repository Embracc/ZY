# -*- coding: utf-8 -*-
"""
cron: 59 59 19 * * *
new Env('雨云抢机子');
"""
import requests
import os
import http.client


yykey = os.environ['yykey']
conn = http.client.HTTPSConnection("api.v2.rainyun.cc:36688")
payload = "{\r\n    \"item_id\": 107\r\n}"
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39",
    'x-api-key': yykey,
    'content-type': "application/json"
    }
conn.request("POST", "/user/reward/items", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

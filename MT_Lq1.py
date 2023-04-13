"""
File: MT_Lq1.py(京东宝藏榜)
Author: HarbourJ
Date: 2022/9/19 22:00
cron: 0 10 * * *
new Env('MT30-15');
ActivityEntry: 首页排行榜-宝藏榜
"""

import requests
import os

ck = os.getenv('MT')
couponReferId='DBFA760914E34AFF9D8B158A7BC4D706'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,ru;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': ck,
    'Origin': 'https://market.waimai.meituan.com',
    'Referer': 'https://market.waimai.meituan.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'mtgsig': '{"a1":"1.0","a2":1681295762249,"a3":"921v698y7698575wy99y6460097z495u813x0247987979585zyu89v1","a4":"f705854b673ebe114b8505f711be3e6702e60c82135832e5","a5":"igYI91o7v+/lG1Sau0Q/+MtG1SosxRmS7c+TUflWC++sl3bbugYR8heFKBpZdzvAH+zNPYqOWUAOI02S76Sv0Eaa5DD=","a6":"h1.2N87MCsncD44bSYJicd979vCQVNuCa3AX5yuSv2OSWSh7dgnrpT4nhn6HC4InTi7ExRqz8ZVTAU0Dzl+davk90rXmpJGFdoB11WHPtn6HPZO+onvDGdNuv7fQxNuwId9QgRQMK0f/f4Gq69PLs2DC5Q9/KFf0zML6DTom69hzTe48cAe5NojQgxZRj4QxUH1Va6cPzxJE9W4JCHkWdJMNnLtBtHNX9XGGo1TZRHzpiI7fHZNQGJ7+h1lksz7rBofaWp6R+ReUA1mJKTvx3WeEq6WZCZtx6b1cIoqQSzMS2Zj15TjbyeJ0mmqh4WksWGK/ozzFT/KvS3xPK0vyI7gbbEyACZeOG8q7s7AXuYSVqbiW3tVLCcXwyQXzpqvR66mjDTBp/epVttHEuCWsTl7OasMUsx/NyJ7DsFEJtWqXyyHjj+Mr4yfA1OQ1spD73PM8b6fgKdPmGxZvSsloLAWnzg==","a7":"","x0":4,"d1":"b38590af1d38d8b998ff2a3a37fe066e"}',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'couponReferId': couponReferId,
    'actualLng': '113.551454',
    'actualLat': '23.32507',
    'geoType': '2',
    'gdPageId': '379391',
    'pageId': '378925',
    'version': '1',
    'utmSource': '70200',
    'utmCampaign': 'wmsq-678762',
    'instanceId': '16619982800580.30892480633143027',
    'componentId': '16619982800580.30892480633143027',
}

json_data = {
    'cType': 'wm_wxapp',
    'fpPlatform': 1,
    'wxOpenId': '',
    'appVersion': '',
    'mtFingerprint': 'H5dfp_1.8.2_tttt_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',
}

response = requests.post(
    'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/fetchcoupon',
    params=params,
    headers=headers,
    json=json_data,
)

print(response.json())

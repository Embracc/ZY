# -*- coding: utf-8 -*-
"""
1 0 * * * 
new Env('阿里云签到');
获取token : https://alist.nn.ci/zh/guide/drivers/aliyundrive.html
环境变量：ali_ck    多账户#隔开
"""

import requests
from os import environ, system, path
from sys import exit


def load_send():
    global send, mg
    cur_path = path.abspath(path.dirname(__file__))
    if path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            print("加载通知服务成功！")
        except:
            send = False
            print("加载通知服务失败~")
    else:
        send = False
        print("加载通知服务失败~")


load_send()


class AliDrive_CheckIn:
    def __init__(self, refresh_token,is_reward):
        self.userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 D/C501C6D2-FAF6-4DA8-B65B-7B8B392901EB"
        self.aliYunPanToken = ''
        self.aliYunPanRefreshToken = ''
        self.refresh_token = refresh_token
        self.msg = ''
        self.user_name = ''
        self.is_reward=is_reward

    def getToken(self):
        url = 'https://auth.aliyundrive.com/v2/account/token'
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        body = {
            "grant_type": "refresh_token",
            "app_id": "pJZInNHN2dZWk8qg",
            "refresh_token": self.refresh_token
        }
        response = requests.post(url, headers=headers, json=body)
        try:
            resp = response.json()
            # print(resp)
            if resp.get('code')=='InvalidParameter.RefreshToken':
                # print('RefreshToken 有误请检查！')
                self.msg += '\nRefreshToken 有误请检查！(可能token失效了，到这里获取https://alist.nn.ci/zh/guide/drivers/aliyundrive.html#%E5%88%B7%E6%96%B0%E4%BB%A4%E7%89%8C)\n'
                return self.msg
                # exit(0)
            else:
                self.aliYunPanToken = f'Bearer {resp["access_token"]}'
                # print(self.aliYunPanToken)
                self.aliYunPanRefreshToken = resp["refresh_token"]
                # print(self.aliYunPanRefreshToken)
                self.user_name = resp["user_name"]

                # print(self.aliYunPanToken)
                # print(self.aliYunPanRefreshToken)
                # print("获取token成功，开始执行签到！")
                self.msg+=f"\n账号：【{self.user_name}】\n获取token成功，开始执行签到！\n"
                # print(f"\n账号：【{self.user_name}】\n获取token成功，开始执行签到！\n")
                self.CheckIn()
                return self.msg
        except:
            # pass
            # print(response.json()["access_token"])
            return response.text
            print(response.text)

    def CheckIn(self):
        sign_url = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
        sign_headers = {
            "Content-Type": "application/json",
            "Authorization": self.aliYunPanToken,
            "User-Agent": self.userAgent
        }
        sign_body = {}
        sign_res = requests.post(sign_url, headers=sign_headers, json=sign_body)
        # print(sign_res.text)
        try:
            sign_resp = sign_res.json()
            # print(sign_resp)
            result = sign_resp['result']
            signInCount = result['signInCount']
            isReward = result['isReward']
            if isReward == True:
                # print(f'签到成功！已累计签到{signInCount}天！')
                self.msg += f'签到成功！已累计签到{signInCount}天！\n'
            else:
                # print(f'今日已签到！已累计签到{signInCount}天！')
                self.msg += f'今日已签到！已累计签到{signInCount}天！\n'
            signInLogs = sign_resp['result']['signInLogs']

            for l in signInLogs:
                # print(f'第{l}天 ')
                if l['status'] != 'miss':
                    cont = f'第{l["day"]}天 '
                    # print(f'第{l["day"]}天 ')
                    if l['reward'] != None:
                        cont += f'获得{l["reward"]["name"]}{l["reward"]["description"]}\n'
                        # print(f'获得{l["reward"]["name"]}{l["reward"]["description"]}\n')
                        # print('开始使用\n')
                        if self.is_reward :
                            cont += self.reward(l["day"])
                    else:
                        cont += "获得了空气！\n"
                        # print("获得了空气！\n")
                    self.msg += cont
            return self.msg
        except:
            print(sign_res)
            # self.msg+=sign_res

    def reward(self, day):
        reward_headers = {
            "Content-Type": "application/json",
            "Authorization": self.aliYunPanToken,
            "User-Agent": self.userAgent
        }
        reward_data = {"signInDay": day}
        response = requests.post('https://member.aliyundrive.com/v1/activity/sign_in_reward', headers=reward_headers,json=reward_data)
        try:
            resp = response.json()
            if resp['result'] != 'null':
                # print(resp['result']['notice'])
                return f"已使用，{resp['result']['notice']}\n"
        except:
            print(response.text)


if __name__ == '__main__':
    refresh_token = ''
    ali_ck = environ.get("ali_ck") if environ.get("ali_ck") else refresh_token
    if ali_ck == "":
        print("未填写refresh_token 青龙可在环境变量设置 ali_ck 或者在本脚本文件上方将获取到的refresh_token填入cookie中")
        exit(0)
    msg = ''
    ali_reward=True
    is_reward = environ.get("ali_reward") if environ.get("ali_reward") else ali_reward
    if is_reward:
        msg += '检测到设置了自动使用奖品\n'
        # print('检测到设置了自动使用奖品\n')
    else:
        msg += '默认不自动使用奖品，如需使用请定义变量：export ali_reward = True\n'
        # print('默认不自动使用奖品，如需使用请定义变量：export ali_reward="True"\n')

    for ck in ali_ck.split("#"):
        Sign = AliDrive_CheckIn(ck,ali_reward)
        msg += Sign.getToken()
    send('阿里云盘签到通知', msg)

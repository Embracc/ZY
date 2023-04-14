import base64
import sys
import requests
import os
from bs4 import BeautifulSoup
import random
 
# 很重要  用session方式  就不用手动处理cookie.注意换账号登陆时候记得清除cookie
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"
}
# 域名请自行解码
domain = "aHR0cHM6Ly93d3cuamF2YXh4ei5jb20="
# 这样开着代{过}{滤}理的时候不会报连接错误  方便测试
os.environ['NO_PROXY'] = domain
#在 https://www.pushplus.plus 免费获取
push_plus_token = "你的token"ocrapi = "http://ip:port"accounts = [{"username": "账号1", "password": "密码1"},
            {"username": "账号2", "password": "密码2"},
            {"username": "账号3", "password": "密码3"},
            {"username": "账号4", "password": "密码4"}
            ]
 
 
#  模拟随机生产五位数字
def getNums(length):
    the_str = ""
    for i in range(length):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        the_str += ch
    return the_str
 
 
# 获取验证码
def getYzmImg():
    rdnum = getNums(5)
    url = f"{domain}/misc.php?mod=seccode&update={rdnum}&idhash=cS"
    getHeader = {"referer": f"{domain}/member.php?mod=logging&action=login&phonelogin=no",
                 "user-agent": headers['User-Agent']}
    get = session.get(url, headers=getHeader)
    # print(get.content)
    # print(f"getYzmImg cookie:{session.cookies}")
    return get.content
 
# 调用搭建的验证码识别api服务.采用这种方式是因为在青龙面板中安装相关依赖失败了.
def decodeYzm(img_types):
    img_base64 = base64.b64encode(img_types).decode()
    # print(img_base64)
    post_headers = {"content-type": "application/json"}
    res = session.post(url=f"{ocrapi}/code/", headers=post_headers, json={'ImageBase64': img_base64})
    # print(res.text)
    return eval(res.text)['result']
 
 
# 获取登陆需要的formhash参数  action时间上好像是定值,不过在form里面就顺便拿过来了
def getLoginParam():
    url = f"{domain}/member.php?mod=logging&action=login&phonelogin=no"
    response = session.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    formhash = soup.find('input', attrs={'name': 'formhash'})["value"]
    action = soup.find('form', attrs={'name': 'login'})["action"]
    # print(f"formhash:{formhash}")
    # print(f"action:{action}")
    param = {"formhash": formhash, "action": action}
    return param
 
# 执行登陆逻辑
def doLoginOnce(param, user, yzm):
    login_dict = {
        "formhash": param['formhash'],
        "referer": f"{domain}/./",
        "loginfield": "username",
        "username": user["username"],
        "password": user["password"],
        "questionid": "0",
        "answer": "",
        "seccodemodid": "member::logging",
        "seccodeverify": yzm
    }
    res = session.post(url=f"{domain}/{param['action']}", headers=headers, data=login_dict)
    # 登陆成功后返回的页面内容会包含用户名
    if user["username"] in res.text:
        # print(f"登陆结果:{res.text}")
        return True
    return False
 
 
# 登陆并签到
def doLoginAndSign(user):
    i = 1
    login_param = getLoginParam()
    login_suc = doLoginOnce(login_param, user, decodeYzm(getYzmImg()))
    # 验证码识别错误,登陆失败的话 重试
    while i < 7 and not login_suc:
        print(f"{user['username']}登陆失败,第{i}次重新尝试")
        login_suc = doLoginOnce(login_param, user, decodeYzm(getYzmImg()))
        i += 1
    if login_suc:
        doSign(user)
 
 
# 执行签到操作
def doSign(user):
    index = session.get(f"{domain}/index.php", headers=headers)
    soup = BeautifulSoup(index.text, "html.parser")
    sign_form_hash = soup.find('input', attrs={'name': 'formhash'})["value"]
    sign_before_action = f"plugin.php?id=dsu_paulsign:sign&{sign_form_hash}&infloat=yes&handlekey=dsu_paulsign&inajax=1&ajaxtarget=fwin_content_dsu_paulsign"
    sign_before_res = session.get(f"{domain}/{sign_before_action}", headers=headers)
    # print(f"签到弹框:{sign_before_res.text}")
    acton = "plugin.php?id=dsu_paulsign%3Asign&operation=qiandao&infloat=1&sign_as=1&inajax=1"
    qd_param = {"formhash": {sign_form_hash}, "qdxq": "kx"}
    res = session.post(url=f"{domain}/{acton}", headers=headers, data=qd_param)
    print(f"{user['username']}签到结果:{res.text}")
    sendNotify(f"java学习{user['username']}签到成功", res.text)
 
 
# 发送微信push_plus消息
def sendNotify(title, content):
    param = {"title": title,
             "content": content,
             "template": "html",
             "token": f"{push_plus_token}",
             }
    requests.post(url="https://www.pushplus.plus/send", headers=headers, data=param)
 
 
if __name__ == '__main__':
    for account in accounts:
        doLoginAndSign(account)
        session.cookies.clear()
    sys.exit(0)

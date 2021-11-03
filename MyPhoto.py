# -*- coding:utf-8 -*-
import hashlib
import json
import random
import time

import requests


def encrypt_pwd(password):
    str_temp = f"tc.everphoto.{password}"
    str_md5 = hashlib.md5(str_temp.encode()).hexdigest()
    return str_md5


def login(country_code, phone, password):
    mobile = f"+{country_code}{phone}"
    pwd = encrypt_pwd(password)

    url = "https://api.everphoto.cn/auth"
    timestamp_ms = str(round(time.time() * 1000))

    payload = {
        'mobile': mobile,
        'password': pwd
    }
    headers = {
        'Host': 'api.everphoto.cn',
        'x-api-version': '20161221',
        'user-agent': 'EverPhoto/2.7.9.1 (Android;2791;Pro 7;23;tengxun_33_1)',
        'x-device-mac': '02:00:00:00:00:00',
        'application': 'tc.everphoto',
        'x-locked': '1',
        'x-timestamp-ms': timestamp_ms,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.loads(response.text)

    return response_data


def logout(token):
    url = "https://api.everphoto.cn/auth"
    timestamp_ms = str(round(time.time() * 1000))

    headers = {
        'Host': 'api.everphoto.cn',
        'x-api-version': '20161221',
        'user-agent': 'EverPhoto/2.7.9.1 (Android;2791;Pro 7;23;tengxun_33_1)',
        'x-device-mac': '02:00:00:00:00:00',
        'application': 'tc.everphoto',
        'authorization': f'Bearer {token}',
        'x-locked': '1',
        'x-timestamp-ms': timestamp_ms
    }

    response = requests.request("DELETE", url, headers=headers)
    response_data = json.loads(response.text)
    code = response_data["code"]
    if code == 0:
        print("退出成功~~~")
    else:
        print(f'退出错误：{response_data["message"]}')


def checkin(token):
    url = "https://api.everphoto.cn/users/self/checkin/v2"
    timestamp_ms = str(round(time.time() * 1000))

    headers = {
        'Host': 'api.everphoto.cn',
        'x-api-version': '20161221',
        'user-agent': 'EverPhoto/2.7.9.1 (Android;2791;Pro 7;23;tengxun_33_1)',
        'x-device-mac': '02:00:00:00:00:00',
        'application': 'tc.everphoto',
        'authorization': f'Bearer {token}',
        'x-locked': '1',
        'x-timestamp-ms': timestamp_ms
    }

    response = requests.request("POST", url, headers=headers)
    response_data = json.loads(response.text)
    code = response_data["code"]
    if code == 0:
        checkin_data = response_data["data"]
        if checkin_data["checkin_result"]:
            reward = checkin_data["reward"]
            capacity = reward // 1048576
            print(f"签到获得{capacity}M空间")
        else:
            print("今日已签到")
    else:
        print(f'签到错误：{response_data["message"]}')


def auto_checkin(country_code, phone, password):
    login_data = login(country_code, phone, password)
    code = login_data["code"]
    if code == 0:
        print(f'登录成功：{login_data["data"]["user_profile"]["name"]}')
        token = login_data["data"]["token"]
        time.sleep(random.randint(800, 1200) / 1000)
        checkin(token)
        time.sleep(random.randint(900, 1400) / 1000)
        logout(token)
    else:
        print(f'登录错误：{login_data["message"]}')


def test():
    print("测试函数")
    # auto_checkin("xxx", "xxx", "xxx")


if __name__ == '__main__':
    test()

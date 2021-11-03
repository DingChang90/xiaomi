# -*- coding:utf-8 -*-
import json

import MyPhoto


def handler(event, context):
    code = context.getUserData("code")
    phone = context.getUserData("phone")
    pwd = context.getUserData("pwd")
    if "+" in code:
        print("国际区号前不要填+号")
    else:
        if code is None or phone is None or pwd is None:
            print("请配置环境变量国际区号、手机号、密码")
        else:
            MyPhoto.auto_checkin(code, phone, pwd)
    output = f'Hello message: {json.dumps(event)}'
    return output

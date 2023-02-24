# -*- coding: utf-8 -*-#
import requests

def send_txt(txt):
    data = {
        "msgtype": "text",
        "text": {
            "content": txt,
            "mentioned_list": [],
        }
    }
    requests.post(url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9f1e25f6-53b1-45ec-a65d-1f23a3840f35',
                  json=data)


if __name__ == "__main__":
    send_txt("bb")

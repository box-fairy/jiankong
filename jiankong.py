# -*- coding: utf-8 -*-

import random
import time
import datetime

# from kuaishou import KuaiShou

from mail import send_mail
from message import send_txt
import os
import configparser
import henhenmao


def find_in_config(owner, author_page_link):
    owner_dict = {}

    if os.path.isfile("jiankong.conf"):
        # 实例化读取配置文件
        cf = configparser.ConfigParser()
        # 用utf-8防止出错
        cf.read("jiankong.conf", encoding="utf-8")
        for k, v in cf["douyin"].items():
            owner_dict[k] = v.split(',')
        if owner in cf["douyin"].keys():
            return author_page_link in owner_dict[owner]
        return False

    return False


class DouYinJianKong(object):
    def __init__(self, author_page_link, owner):
        self.owner = owner
        self.author_page_link = author_page_link
        self.saved_posts = None

    def start(self, interval):

        while True:
            if not find_in_config(self.owner, self.author_page_link):
                send_txt("退出监控：" + dy.nickname)
                break

            new_video_urls = []
            new_captions = []

            print(str(datetime.datetime.now()) + " " + self.author_page_link)
            posts, nickname = henhenmao.get_dy_profile()

            for a_post in posts:
                if self.saved_posts and a_post not in self.saved_posts:
                    # index = dy.aweme_ids.index(aweme_id)
                    new_video_urls.append(a_post['medias']['resource_url'])
                    new_captions.append(a_post['text'])

            self.saved_posts = posts

            # print("当前：", dy.captions)
            # print("新的：", new_captions)
            # print("新的：%s", new_ video_urls)

            if new_video_urls:
                # owner（我需要搬运到自己的账户）可以有多个，这里进行随机选择
                owners = self.owner.split(',')
                random_owner = random.sample(owners, 1)
                send_mail(random_owner + "\r" + dy.nickname + "\r" + self.author_page_link,
                          new_captions[0] + "\r" + new_video_urls[0])
                send_txt("监控到新动态：" + nickname + " " + new_captions[0])
            else:
                send_txt("没有新动态：" + nickname)

            current_hour = int(datetime.datetime.now().strftime('%H'))
            if current_hour == 0:
                time.sleep(3600 * 7)
            else:
                time.sleep(interval)
                # time.sleep(interval + random.randint(-60, 60))


# class KuaiShouJianKong(object):
#     def __init__(self, author_id, owner, jiankong_list): # jiankong_list是用来控制是否应该无限循环的
#         self.owner = owner
#         self.author_id = author_id
#         self.jiankong_list = jiankong_list
#         self.saved_captions = []
#
#     def start(self, interval):
#         ks = KuaiShou(self.author_id)
#         ks.phase()
#         print(ks.captions, ks.video_urls)
#         self.saved_captions = ks.captions
#         time.sleep(interval + random.randint(-60, 60))
#         # time.sleep(interval)
#
#         if (self.author_id, self.owner) in self.jiankong_list:
#             video_urls = []
#             captions = []
#
#             ks = KuaiShou(self.author_id)
#             ks.phase()
#             for caption in ks.captions:
#                 if caption not in self.saved_captions:
#                     index = ks.captions.index(caption)
#                     video_urls.append(ks.video_urls[index])
#                     captions.append(ks.captions[index])
#
#             self.saved_captions = ks.captions
#             print(captions)
#             print(video_urls)
#
#             if video_urls:
#                 send_mail(self.owner + "\r" + "快手作者" + self.author_id, captions[0] + "\r" + video_urls[0])
#
#             time.sleep(interval + random.randint(-60, 60))


if __name__ == "__main__":
    douyin = DouYinJianKong("https://v.douyin.com/h69u4kj/", "包叔吃货铺")
    douyin.start(60)

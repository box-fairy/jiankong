# -*- coding: utf-8 -*-
from jiankong import DouYinJianKong
# from jiankong import KuaiShouJianKong
import threading
from message import send_txt
import time
import configparser
import os

#监控对标首页间隔时间
jiankong_douyin_interval = 900
#监控线程间隔时间
jiankong_thread_interval = 300


def jankong_douyin(author_page_link, shipinhao_acount_name):
    douyin = DouYinJianKong(author_page_link, shipinhao_acount_name)
    douyin.start(jiankong_douyin_interval)


# def jankong_kuaishou(author_id, owner, jiankong_list):
#     kuaishou = KuaiShouJianKong(author_id, owner, jiankong_list)
#     kuaishou.start(7200)


def count_thread():
    thread_count = len(threading.enumerate()) - 1
    send_txt("监控数量： %d" % thread_count)


def read_config():
    onwer_dict = {}

    if os.path.isfile("jiankong.conf"):
        # 实例化读取配置文件
        cf = configparser.ConfigParser()
        # 用utf-8防止出错
        cf.read("jiankong.conf", encoding="utf-8")
        for k, v in cf["douyin"].items():
            onwer_dict[k] = v.split(',')

    return onwer_dict


if __name__ == "__main__":

    jiankong_list_current = {}

    while True:
        count_thread()
        jiankong_list_next = {}
        # 从 config 读入字典。
        owners_douyin = read_config()

        # 从字典生成新列表，线程名全部为空。
        for owner in owners_douyin:
            for page in owners_douyin[owner]:
                jiankong_list_next[(page, owner)] = None

        # 遍历老列表，把老列表的对应线程名复制到新列表。
        found = False
        for a_old_jiankong in jiankong_list_current:
            for a_new_jiankong in jiankong_list_next:
                if a_old_jiankong == a_new_jiankong:
                    found = True
                    jiankong_list_next[a_new_jiankong] = jiankong_list_current[a_old_jiankong]
                    break

        # 将新列表复制给老列表，遍历老列表，如果有线程不在现有线程池活动，则启动。
        jiankong_list_current = jiankong_list_next

        for args, thread_name in list(jiankong_list_current.items()):
            active = False
            for thread_info in threading.enumerate():
                if thread_name == thread_info.name:
                    active = True
            if not active:
                page = args[0]
                owner = args[1]
                send_txt("加入监控： " + page)
                #启动监控线程
                thread = threading.Thread(target=jankong_douyin, args=(page, owner))
                time.sleep(1)
                jiankong_list_current[args] = thread.name
                print(jiankong_list_current)
                thread.start()
                count_thread()

        time.sleep(jiankong_thread_interval)

    # for owner in owners_douyin:
    #     for page in owners_douyin[owner]:
    #         thread = threading.Thread(target=jankong_douyin, args=(page, owner))
    #         jiankong_list[thread.name] = (page, owner)
    #         thread.start()

    # 永久循环，监控是否有监控线程丢失，如有丢失则重启根
    # while True:
    #     count_thread()
    #     for thread_name, args in list(jiankong_list.items()):
    #         alive = False
    #         for thread_info in threading.enumerate():
    #             if thread_name == thread_info.name:
    #                 alive = True
    #         if not alive:
    #             page = args[0]
    #             owner = args[1]
    #             send_txt("重启监控： " + page)
    #             thread = threading.Thread(target=jankong_douyin, args=(page, owner))
    #             jiankong_list.pop(thread_name)
    #             jiankong_list[thread.name] = (page, owner)
    #             print(jiankong_list)
    #             thread.start()
    #             count_thread()
    #
    #     time.sleep(300)

    # for owner in owners_kuaishou:
    #     for author_id in owners_kuaishou[owner]:
    #         thread = threading.Thread(target=jankong_kuaishou, args=(author_id, owner))
    #         thread.start()

    # thread = threading.Thread(target=jankong_kuaishou, args=("3xfdb6tws2j5r6m", "包叔吃货铺"))
    # thread.start()
    # #
    # # kuaishou = KuaiShouJianKong("3xfdb6tws2j5r6m", "包叔吃货铺")
    # # kuaishou.start(7200)

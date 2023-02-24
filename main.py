# -*- coding: utf-8 -*-
from jiankong import DouYinJianKong
from jiankong import KuaiShouJianKong
import threading
from message import send_txt
import time
import configparser

# owners_douyin = {"包叔吃货铺": ["https://v.douyin.com/25474Vx",
#                           "https://v.douyin.com/25CnurX/"], }
owners_douyin = {
    "包叔吃货铺": ["https://v.douyin.com/2y8BJfY/",
              "https://v.douyin.com/27Ghrvd/",
              "https://v.douyin.com/2y8nyhE/",
              "https://v.douyin.com/2y8sQ7d/",
              # "https://v.douyin.com/27nTxxK/",
              "https://v.douyin.com/27W8khu/"],
    "益智小神童": ["https://v.douyin.com/M81moF3/",
              "https://v.douyin.com/M8eBFHJ/"],
    "精致露营攻略": ["https://v.douyin.com/27sDsxq/"],
    # "https://v.douyin.com/27sNPDe/"],
    # "豆奶是只喵": ["https://v.douyin.com/jSxMj6n/",
    #           "https://v.douyin.com/jSxs6fR/",
    #           "https://v.douyin.com/jSxHFBx/"],
}


# owners_kuaishou = {"包叔吃货铺": ["3xfdb6tws2j5r6m",
#                              "3xfdb6tws2j5r6m",
#                              "3xfdb6tws2j5r6m",
#                              "3xfdb6tws2j5r6m"], }


def jankong_douyin(author_page_link, owner):
    douyin = DouYinJianKong(author_page_link, owner)
    douyin.start(900)


def jankong_kuaishou(author_id, owner):
    kuaishou = KuaiShouJianKong(author_id, owner)
    kuaishou.start(7200)


def count_thread():
    thread_count = len(threading.enumerate()) - 1
    send_txt("监控数量： %d" % thread_count)


if __name__ == "__main__":
    threads_name = {}

    # 根据字典，启动监控对标
    for owner in owners_douyin:
        for page in owners_douyin[owner]:
            thread = threading.Thread(target=jankong_douyin, args=(page, owner))
            threads_name[thread.name] = (page, owner)
            thread.start()

    # 永久循环，监控是否有监控线程丢失，如有丢失则重启根
    while True:
        count_thread()
        for thread_name, args in list(threads_name.items()):
            alive = False
            for thread_info in threading.enumerate():
                if thread_name == thread_info.name:
                    alive = True
            if not alive:
                page = args[0]
                owner = args[1]
                send_txt("重启监控： " + page)
                thread = threading.Thread(target=jankong_douyin, args=(page, owner))
                threads_name.pop(thread_name)
                threads_name[thread.name] = (page, owner)
                print(threads_name)
                thread.start()
                count_thread()

        time.sleep(300)

    # for owner in owners_kuaishou:
    #     for author_id in owners_kuaishou[owner]:
    #         thread = threading.Thread(target=jankong_kuaishou, args=(author_id, owner))
    #         thread.start()

    # thread = threading.Thread(target=jankong_kuaishou, args=("3xfdb6tws2j5r6m", "包叔吃货铺"))
    # thread.start()
    # #
    # # kuaishou = KuaiShouJianKong("3xfdb6tws2j5r6m", "包叔吃货铺")
    # # kuaishou.start(7200)

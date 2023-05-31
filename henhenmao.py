import requests

hhm_api = 'https://h.aaaapp.cn/posts'  # 单个帖子提取接口 (如果主页批量提取使用：https://h.aaaapp.cn/posts)
user_id = '0AC8C1EC28EA5DBD46B0795EB7DB51B5'  # 这里改成你自己的 userId
secret_key = '5583b23c31ce281b4484e1272e9327ef'  # 这里改成你自己的 secretKey


def get_dy_profile():
    # 参数
    url = 'https://v.douyin.com/Dw9mTga/'

    params = {
        'userId': user_id,
        'secretKey': secret_key,
        'url': url
    }
    r = requests.post(hhm_api, json=params, verify=False)
    print(r.json()['data']['posts'])
    return r.json()['data']['posts'], r.json()['data']['user']['username']


if __name__ == "__main__":
    get_dy_profile()

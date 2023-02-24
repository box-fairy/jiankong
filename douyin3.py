from Util import Profile
import Util


class DouYin(Profile):

    def __init__(self, author_page_link):
        super().__init__()

        self.uid = author_page_link
        self.aweme_ids = []
        self.video_urls = []
        self.captions = []

    def getProfile(self):
        Profile.getProfile(self, (self.uid, 'no', 'post'))
        self.aweme_ids = self.aweme_id
        self.captions = self.author_list
        for video_url in self.uri_list:
            self.video_urls.append('https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&ratio=1080p&line=0' % video_url)

        print(self.nickname, self.captions, self.video_urls)

    def getVideoInfo(self, result):
        """获取视频信息
        """
        # 作者信息
        self.author_list = []
        # 无水印视频链接
        # self.video_list = []
        # 作品id
        self.aweme_id = []
        # 唯一视频标识
        self.uri_list = []
        # 图集
        self.image_list = []
        # 封面大图
        # self.dynamic_cover = []
        for v in range(len(result)):
            try:
                # url_list < 4 说明是图集
                # 2022/11/27 aweme_type是作品类型 2：图集 4：视频
                if result[v]['aweme_type'] == 2:
                    # if len(result[v]['video']['play_addr']['url_list']) < 4:
                    self.image_list.append(result[v]['aweme_id'])
                else:
                    self.author_list.append(str(result[v]['desc']))
                    # 2022/04/22
                    # 如果直接从 /web/api/v2/aweme/post 这个接口拿数据，那么只有720p的清晰度
                    # 如果在 /web/api/v2/aweme/iteminfo/ 这个接口拿视频uri
                    # 拼接到 aweme.snssdk.com/aweme/v1/play/?video_id=xxxx&radio=1080p 则获取到1080p清晰的
                    # self.video_list.append(
                    #     str(result[v]['video']['play_addr']['url_list'][0]))
                    self.uri_list.append(
                        str(result[v]['video']['play_addr']['uri']))
                    self.aweme_id.append(str(result[v]['aweme_id']))
                    # nickname.append(str(result[v]['author']['nickname']))
                    # self.dynamic_cover.append(str(result[v]['video']['dynamic_cover']['url_list'][0]))
            except Exception as e:
                # 输出日志
                Util.log.info('%s,因为每次不一定完全返回35条数据！' % (e))
                print('[  🚩  ]:%s,因为每次不一定完全返回35条数据！' % (e))
                break
        if self.max_cursor == 0:
            return
        # 过滤视频文案和作者名中的非法字符
        print('[  提示  ]:等待替换文案非法字符!\r')
        self.author_list = Util.replaceT(self.author_list)
        # 输出日志
        Util.log.info('[  提示  ]:等待替换文案非法字符!')

        print('[  提示  ]:等待替换作者非法字符!\r')
        self.nickname = Util.replaceT(self.nickname)
        # 输出日志
        Util.log.info('[  提示  ]:等待替换作者非法字符!')
        # 下载主页所有图集
        datas = Util.Images().get_all_images(self.image_list)
        # Util.Download().VideoDownload(self)
        # Util.Download().ImageDownload(datas)
        # self.getNextData()
        return  # self,author_list,video_list,uri_list,aweme_id,nickname,max_cursor


if __name__ == "__main__":
    DY = DouYin("https://v.douyin.com/25CnurX/")
    DY.getProfile()
    # DY.judge_link()
    # print(DY.captions, DY.video_urls)

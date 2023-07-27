## simple jiuse video or 91 video scrapy and download


### jiuse视频发布网址：https://dz91.gitbook.io/jiuse/
1. 抓取九色视频本月最热、搜索等获取视频列表

2. 对抓取的列表中视频进行下载


### 代码说明
1. 视频列表保存到本地demo.json中
2. video_list.py用于获取视频列表
3. m3u8_download.py用于下载指定m3u8链接的视频，且转换为mp4格式
4. video_download.py用于下载指定视频链接的视频，且保存在指定格式


### 更新说明：
1. 2023-07-26： 处理ffpemg无法直接保存中文名称的视频问题
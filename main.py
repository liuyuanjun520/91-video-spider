# coding: utf-8

"""
@author: JankoKaKa
@software: PyCharm
@file: main.py
@time: 2023/8/4 19:40
"""

from utils.video_list import VideoListObj
from utils.video_download import VideoDownload
import webbrowser
from utils.send_telegrame import send_data


class MainControl:
    """主进程"""

    def play_m3u8_link(self, url_link):
        m3u8_link_prefix = 'https://tool.liumingye.cn/m3u8/#'
        webbrowser.open(m3u8_link_prefix + url_link)
        print('打开成功')

    def main_run(self, authority, line_which='line1'):
        # 参数authority为网站域名，如jstv7.cc
        # 参数line_which为线路选择，如line1

        v_list_obj = VideoListObj()
        v_download_obj = VideoDownload()

        close_flag = False
        while close_flag is False:
            input_text = input('请输入序号,0退出, 1:本月最热\n')
            if input_text == '0':
                close_flag = True
            elif input_text == '1':

                page = 1
                close_flag_second = False

                while close_flag_second is False:
                    all_video_list = []
                    # 第一次进行获取第一页以及，最大页数
                    html_text = v_list_obj.get_list_html(authority, page)
                    page_one_list = v_list_obj.parse_list_html(html_text)
                    page_info = v_list_obj.parse_page_html(html_text)
                    all_video_list.extend(page_one_list)
                    print(f'max:{page_info.get("max_page", 1)}')

                    # 展示第一页数据
                    count = 0
                    # current_list = []
                    for item in page_one_list:
                        # print(f'{count}::title:{item.get("title", "no title")}**[{item.get("duration", "no dura")}]')
                        # 发送到telegame
                        view_link = 'https://' + authority + item.get('href', '')
                        # background = 'https://' + item.get('background', '')
                        send_data(f'title:{item.get("title", "no title")}**[{item.get("duration", "no dura")}]\nlink:{view_link}')
                        count += 1
                    print(f'当前页:{page}')

                    input_text_second = input('请输入序号,0退出, 1:下一页, 2:上一页, 3:打开m3u8链接\n')
                    if input_text_second == '0':
                        close_flag_second = True
                    elif input_text_second == '1':
                        page += 1
                    elif input_text_second == '2':
                        page -= 1
                    elif input_text_second == '3':
                        input_text_third = input('请输入序号,0退出, 1:打开m3u8链接\n')
                        temp_item = page_one_list[int(input_text_third)]
                        temp_m3u8_link = v_download_obj.get_video_html_and_parse_m3u8(
                            'https://' + authority,
                            temp_item,
                            line_which
                        )
                        print(temp_m3u8_link)
                        self.play_m3u8_link(temp_m3u8_link)
                        input('回车继续')
                    else:
                        print('请重输入有效数字')





            else:
                print('请重输入有效数字')
        print('退出')


if __name__ == '__main__':
    obj = MainControl()
    obj.main_run('jstv7.cc')

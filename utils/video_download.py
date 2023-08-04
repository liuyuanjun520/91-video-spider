# coding: utf-8

"""
@author: JankoKaKa
@software: PyCharm
@file: video_download.py
@time: 2023/7/26 19:02
"""
import json
import time
import requests
from bs4 import BeautifulSoup
from utils.m3u8_download import M3u8Download


class VideoDownload:

    def get_list(self):
        """获取视频列表"""
        file_name = '../demo.json'
        with open(file_name, "r") as json_file:
            data_list = json.load(json_file)

        return data_list

    def get_video_html_and_parse_m3u8(self, url_prefix, data_item, server_str=None):
        """获取视频惠html，且从链接中获取播放m3u6地址"""

        if data_item.get('href', None):
            # url = "https://jstv7.cc/video/view/161a9d8eccf1946fd684?server=line1"
            # url_prefix = 'https://jstv7.cc'
            url = url_prefix + data_item.get('href', None) + ('?server=' + server_str if server_str else '')

            payload = {}
            headers = {
                'authority': url_prefix.split('//')[1],
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'cookie': 'promotion=org; JSESSIONID=44422264379aa01a06a285939c721a90; wms=1; Hm_lvt_e0919deb04df7ddb45bf6e9d8b83a614=1690360430; _gid=GA1.2.1002891127.1690360433; Hm_lpvt_e0919deb04df7ddb45bf6e9d8b83a614=1690362747; _ga_F8MXJQGLN1=GS1.1.1690360429.1.1.1690362747.0.0.0; _ga=GA1.2.1284590192.1690360430; JSESSIONID=44422264379aa01a06a285939c721a90',
                'pragma': 'no-cache',
                'referer': 'https://jstv7.cc',
                'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }

            response = requests.request("GET", url, headers=headers, data=payload, verify=False)

            if response.status_code < 300:
                html_str = response.text
                soup = BeautifulSoup(html_str, 'html.parser')
                data_src = soup.find('video', id='video-play')['data-src']
                data_src = data_src.replace('&amp;', '&')
                # print(data_src)
                return data_src

            else:
                print('ERR, 视频html请求错误 status_code:', response.status_code)
                return None

    def download_video(self, d_url, save_path, name):
        """视频下辖"""
        try:

            M3u8Download(d_url, name, save_path, max_workers=64, num_retries=5)
        except Exception as e:
            print('ERR, 视频下载错误', e)

    def main_run(self, url_p, save_path):
        data_list = self.get_list()

        for item in data_list:
            d_url = self.get_video_html_and_parse_m3u8(url_p, item, 'line1')
            if d_url:
                print(f'download:{item.get("title", "-1")}')
                self.download_video(d_url, save_path, item.get("title", str(int(time.time()))))
                print('download success')
                # return True
                time.sleep(10)


if __name__ == '__main__':
    obj = VideoDownload()
    # save_path = os.getcwd()
    save_path_ = r'D:\jiuse\202307'
    obj.main_run('https://jstv7.cc', save_path_)

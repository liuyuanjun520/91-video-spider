# coding: utf-8

"""
@author: JankoKaKa
@software: PyCharm
@file: video_list.py
@time: 2023/7/26 17:38
"""
import json
import time

import requests
from bs4 import BeautifulSoup


class VideoListObj:
    """抓取指定jiuse视频列表数据，生成一个个url链接地址"""

    def get_list_html(self, authority, page):
        """
        获取指定html界面中的html
        :param
            authority:  jstv7.cc 域名中内容
        """
        url = f"https://jstv7.cc/video/category/top-list/{page}"

        payload = {}
        headers = {
            'authority': authority,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            # 'Cookie': 'JSESSIONID=44422264379aa01a06a285939c721a90'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code < 300:
            # print(response.text)
            return response.text
        else:
            print(f"获取{url}失败，状态码：{response.status_code}")
            return None

    def parse_list_html(self, html_str):
        """解析html内容，获取所有指定视频链接"""
        soup = BeautifulSoup(html_str, 'html.parser')
        list_elements = soup.find_all(class_='colVideoList')
        print(len(list_elements))
        final_list = []
        for item in list_elements:
            try:
                temp_href = item.find('a')['href']
                temp_title = item.find('div', class_='img')['title']
                temp_duration = item.find(class_='layer').text
                background = item.find('div', class_='img')['style']

                final_list.append({
                    'href': temp_href,
                    'title': temp_title,
                    'duration': temp_duration,
                    'background': background.split('url(')[1].split(')')[0]
                })

            except Exception as e:
                continue

        return final_list

    def parse_page_html(self, html_str):
        """解析html内容，获取列表长度"""
        soup = BeautifulSoup(html_str, 'html.parser')
        list_elements = soup.find_all('ul', class_='pagination')
        # print(len(list_elements))
        final_list = []
        for item in list_elements:
            all_pages = item.find_all('li')
            for li_item in all_pages:
                if li_item.text.isdigit():
                    try:
                        final_list.append(int(li_item.text))
                    except Exception as e:
                        continue
        if not final_list:
            final_list = [1]
        return {
            "max_page": max(final_list)
        }

    def save_json(self, data):
        """保存list数据为json"""

        file_name = '../demo_1.json'
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def main_run(self, authority):
        page = 1
        sleep_delay = 1
        all_video_list = []

        try:
            # 第一次进行获取第一页以及，最大页数
            html_text = self.get_list_html(authority, page)
            page_one_list = self.parse_list_html(html_text)
            page_info = self.parse_page_html(html_text)
            all_video_list.extend(page_one_list)
            print(f'max:{page_info.get("max_page", 1)}')

            # 展示第一页数据
            for item in page_one_list:
                print(f'title:{item.get("title", "no title")}**[{item.get("duration", "no dura")}]')
                temp_link = 'https://' + authority + item.get('href', '')
                print(f'link:{temp_link}')

            # 循环获取
            # while page_info.get("max_page", 1) > page:
            #     page += 1
            #
            #     html_text = self.get_list_html(authority, page)
            #     item_list = self.parse_list_html(html_text)
            #     all_video_list.extend(item_list)
            #     print(f'finished:{page}, max:{page_info.get("max_page", 1)}')
            #     time.sleep(sleep_delay)

            # 存储
            self.save_json(all_video_list)
            print('list加载完成')
            return all_video_list
        except Exception as e:
            print(f'ERR, {e.args}')
            self.save_json(all_video_list)


if __name__ == '__main__':
    authority = 'jstv7.cc'

    obj = VideoListObj()
    # html_text = obj.get_list_html(authority, 1)
    obj.main_run(authority)
    # print(d)

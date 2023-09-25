# coding: utf-8

"""
@author: JankoKaKa
@software: PyCharm
@file: send_telegrame.py
@time: 2023/8/4 20:59
"""
import requests


def send_photo_and_message(token, chat_id, message_text):
    send_message_url = f'https://api.telegram.org/bot{token}/sendMessage'

    # 发送文本消息
    message_data = {
        'chat_id': chat_id,
        'text': message_text
    }
    requests.post(send_message_url, data=message_data)


def send_data(message_text):
    """发送图文消息到telegramd-机器人"""
    telegram_token = "6665078013:AAGwtzclniEnHnxkZQWtslC-_kgnFXN2csc"  # 替换为你的Telegram Bot API令牌
    chat_id = "-905878649"  # 替换为你的目标聊天ID
    send_photo_and_message(telegram_token, chat_id, message_text)


if __name__ == '__main__':
    photo_url = "https://int.ucloud12.xyz/thumb/860031.webp"  # 替换为你的图片URL
    message_text = "Hello, this is a photo and message from Python using requests!"  # 要发送的消息内容
    send_data(message_text)

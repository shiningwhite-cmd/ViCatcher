import asyncio
import os
import threading
import queue
import time
import json

from metagpt.logs import logger

saved_path_a = 'Data/Intermediary/search_video_match.txt'
saved_path_b = 'Data/Intermediary/final_dict.txt'

class Intermediary:
    """"""
    text_queue: any = None
    text_queue_len: int = 0
    last_item: str = None
    concept_dict: dict = None
    search_video_match: dict = None

    def __init__(self):
        super().__init__()

        self.text_queue = queue.Queue()
        self.text_queue_len = 0

        logger.info("init!")

        self.search_video_match = self.read_from_txt(saved_path_a)
        self.concept_dict = self.read_from_txt(saved_path_b)

        pass

    @staticmethod
    def save_to_txt(data, saved_path):
        # 将字典转换为JSON格式的字符串
        json_data = json.dumps(data)

        # 将JSON字符串写入到文本文件中
        with open(saved_path, 'w') as file:
            file.write(json_data)

        return

    @staticmethod
    def read_from_txt(saved_path):
        # 打开文件并读取JSON数据
        with open(saved_path, 'r') as file:
            data_string = file.read()
            if data_string == '':
                return None
            return json.loads(data_string)

    @staticmethod
    def clear_full_txt(saved_path):
        # 打开文件以写入模式，这会清空文件内容
        with open(saved_path, 'w') as file:
            # 由于我们使用了'w'模式，这里不需要写入任何内容
            pass

    def clear_all_saved_data(self):
        self.clear_full_txt(saved_path_a)
        self.clear_full_txt(saved_path_b)

    def put_queue(self, text: str) -> None:
        """get message from outside and store in queue."""
        self.text_queue.put(text)
        self.text_queue_len = int(self.text_queue_len + 1)
        self.last_item = text

        return

    def get_queue(self) -> str:
        """put the message to outside and delete it"""
        if self.text_queue_len > 0:
            self.text_queue_len = int(self.text_queue_len - 1)
            return self.text_queue.get()

    def queue_is_not_none(self) -> bool:
        """"""
        if self.text_queue_len > 0:
            return True

        return False

    def get_last_item(self):

        return self.last_item

    def set_video_info(self, final_dict, search_video_match):
        self.search_video_match = search_video_match
        self.concept_dict = final_dict

        logger.info("saving!")
        self.save_to_txt(search_video_match, saved_path_a)
        self.save_to_txt(final_dict, saved_path_b)
        logger.info("saved!")

    def get_video_info(self):
        return self.search_video_match, self.concept_dict


#!/usr/bin/env python
"""
@Modified By: sw, 2024/02/29, use Google api as search engine and add searching sites restriction.
"""

from __future__ import annotations

import asyncio
import requests
import os
from typing import List

import time
from metagpt.actions import Action
from metagpt.logs import logger

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_search import YoutubeSearch
import json

FOLDER_PATH = "Data/FavoriteFolder/"
DATA_FORMAT = ".json"

KNOWLEDGE_TRANSFER = """
Organize the content of the article below into points of storage
{context}

---
Here's your organized knowledge:
"""


class YoutubeVideoSearch(Action):
    json_list: List[str] = []
    @staticmethod
    def download_video_srt(video_id: str) -> any:
        # 视频的YouTube ID
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=['en', 'zh-Hans'])

        return transcript_list

    @staticmethod
    def arrange_srt_into_text(srt):
        text = ""
        for clip in srt:
            text = text + clip['text']

        return text

    @staticmethod
    def search_youtube_video(keyword: str, max_results: int = 5):
        # 返回一个字典
        results = YoutubeSearch(keyword, max_results=max_results).to_dict()

        return results

    @staticmethod
    def safe_into_json(context: str, file_name: str, video_id: str):
        # 创建一个包含文本信息的字典
        data = {
            "video_id": video_id,
            "knowledge": context
        }
        file_path = FOLDER_PATH + file_name

        # 检查文件是否存在
        if os.path.exists(file_path):
            # 如果文件已存在，打开文件并读取数据
            with open(file_path, 'r') as file:
                existing_data = json.load(file)

            # 将新数据添加到现有数据中
            existing_data.append(data)

            # 写入更新后的数据回文件
            with open(file_path, 'w') as file:
                json.dump(existing_data, file, indent=4)
        else:
            # 如果文件不存在，创建新文件并存入数据
            with open(file_path, 'w') as file:
                json.dump([data], file, indent=4)

    def get_json_list(self):
        # 文件夹路径
        dir_path = FOLDER_PATH

        # 存储文件名的列表
        files = []

        # 遍历文件夹
        for file_path in os.listdir(dir_path):
            # 检查当前文件路径是否是文件
            if os.path.isfile(os.path.join(dir_path, file_path)):
                # 将文件名添加到列表中
                files.append(file_path)

        # 存储所有的数据名称
        self.json_list = files

    def match_json_list(self, keyword: str):
        data_list = set(self.json_list)

        if keyword in data_list:
            pass
        

    async def knowledge_collect(self, keyword: str, video_id: str, context: str):
        prompt = KNOWLEDGE_TRANSFER.format(context=context)

        knowledge = await self.llm.aask(prompt)

        logger.info(knowledge)

        self.safe_into_json(knowledge, keyword, video_id)




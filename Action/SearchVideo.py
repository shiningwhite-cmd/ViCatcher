#!/usr/bin/env python
"""
@Modified By: sw, 2024/02/29, use Google api as search engine and add searching sites restriction.
"""

from __future__ import annotations

import asyncio
import requests
import os
import re
from typing import List

import time
from metagpt.actions import Action
from metagpt.logs import logger

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_search import YoutubeSearch
import youtube_dl
import json
import nltk
from keybert import KeyBERT
from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity


FOLDER_PATH = "Data/FavoriteFolder/"
DATA_FORMAT = ".json"

KNOWLEDGE_TRANSFER = """
Organize the content of the article below into points of storage
{context}

---
Here's your organized knowledge:
"""

PRE_CONCEPT_SEARCH = """
Now I am searching for study material on topic {topic}. I want to get more background concepts and \
upper conceptual knowledge about topic {topic}. Your suggested keywords must conceptually include topic {topic}. 
For example, when the user's search term is "C# language", your suggested keyword could be "advanced programming language" \
or "programming language". Please suggest me a keyword that matches the criteria: 
"""

GOAL_COLLECT = """# Requirement
Now you are watching a video for learning, and the main context of this video will provided in the "Context" section.\
You should use the main context to develop learning goals for this video learning. The goals you develop should include\
 "What you want to learn" and "What knowledge you can learn in this video". Please present the goals in the format \
found in the "Format" section. Present the final result, the goals you develop, in the "Goals" section.

# Context
{context}

# Format
- (First Goal ...)
- (Second Goal ...)
- (Third Goal ...)
- (Forth Goal ...)
- ...

# Goals 
"""

# CONCEPT_COLLECT = """# Requirement
# Now you are watching a video to learn something about {topic}, and the main context of this video will provided \
# in "Context" section. You should use the context to extract the main concepts included in this video learning. \
# Please present the goals in the format found in "Format" section. \
# Present the final result, the goals you develop, in the "Goals" section.
#
# # Context
# {context}
#
# # Format
# - (First Concept ...)
# - (Second Concept ...)
# - (Third Concept ...)
# - (Forth Concept ...)
# - ...
#
# # Concepts
# """
#
# """The concepts you develop should include "The main knowledge in the topic {topic}" and \
# "The main knowledge you can learn in this video". """

SUMMARY_COLLECT = """# Context
{context}

# Requirement
Now you are watching a video to learn something about {topic}, and the main context of this video will provided \
in "Context" section. You should use the context to make a point-by-point summary for this video learning. \
Be careful to reflect the subjective content of learning, i.e. the video is to be the "subject" of our learning. \
Please present the goals in the format found in "Format" section. 

# Format
- (First Point ...)
- (Second Point ...)
- (Third Point ...)
- (Forth Point ...)
- ...
"""

CONCEPT_COLLECT = """# Summary
{summary}

# Requirement
Now you are watching a video to learn something about {topic}, and the main summary of this video will provided \
in "Summary" section. You need to extract the key concepts involved within this video using the provided summary. \
Key concepts refer to specialized vocabulary or expertise that is mentioned and has relevance to the topic {topic}. \
The concept takes the form of a ** noun phrase ** containing the "subject" of learning. This noun phrase will show \
the ** highlight you can learn from this video ** . You need to make the narrative as concise as possible, \
for example, if a video on learning to code summarizes the point as 'Control flow with if statements and loops', \
you can just simplify it to 'if statements and loops' because 'if statements and loops' is a noun phrase \
that refers to a type of program syntax Please present the goals in the format found in "Format" section. 

# Format
- (First Key concepts ...)
- (Second Key concepts ...)
- (Third Key concepts ...)
- (Forth Key concepts ...)
- ...
"""


class YoutubeVideoSearch(Action):
    json_list: List[str] = []

    @staticmethod
    def download_video_srt(video_id: str) -> any:
        # 视频的YouTube ID
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        except Exception:
            logger.info(Exception)
            return
        else:
            return transcript_list

    @staticmethod
    def arrange_srt_into_text(srt):
        if srt is not None:
            text = ""
            for clip in srt:
                text = text + clip['text']
            return text

        return

    @staticmethod
    def search_youtube_video(keyword: str, max_results: int = 5):
        # 返回一个字典
        results = YoutubeSearch(keyword, max_results=max_results).to_dict()

        return results

    @staticmethod
    def get_title_from_id(video_id: str) -> str:
        # 使用youtube-dl获取视频信息
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)

        # 获取视频标题
        video_title = video_info.get('title', None)

        return video_title

    @staticmethod
    def save_into_json(context: str, file_name: str, video_id: str):
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

    @staticmethod
    def dict_merge(dict1: {}, dict2: {}, similarity: int = 0.6):

        # 加载预训练的BERT模型和分词器
        tokenizer = BertTokenizer.from_pretrained("Models/bert-base-uncased", local_files_only=True)
        model = BertModel.from_pretrained("Models/bert-base-uncased", local_files_only=True)

        # 将两个字典合并为一个
        merged_dict = {**dict1, **dict2}
        merged_list = list(merged_dict)

        # 获取每个词汇的BERT嵌入
        embeddings = []
        for word in merged_list:
            inputs = tokenizer(word, return_tensors='pt')
            outputs = model(**inputs)
            embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy())

        # 计算余弦相似度
        similarity_matrix = cosine_similarity(embeddings)

        # 创建一个字典来存储相似词汇的分组
        similar_words = {}
        ori_dict = {}

        # 遍历相似度矩阵，找到相似的词汇
        for i in range(len(merged_list)):
            ori_dict[merged_list[i]] = merged_dict[merged_list[i]]
            for j in range(i + 1, len(merged_list)):
                if similarity_matrix[i][j] > similarity:  # 假设相似度阈值为0.9
                    if merged_list[i] not in similar_words:
                        similar_words[merged_list[i]] = [merged_list[j]]
                        if merged_dict[merged_list[j]] not in ori_dict[merged_list[i]]:
                            ori_dict[merged_list[i]].extend(merged_dict[merged_list[j]])
                    else:
                        similar_words[merged_list[i]].append(merged_list[j])
                        if merged_dict[merged_list[j]] not in ori_dict[merged_list[i]]:
                            ori_dict[merged_list[i]].extend(merged_dict[merged_list[j]])

        # 创建一个新的列表，只保留每个组中的一个词汇
        final_list = list(similar_words.keys())
        final_ori_dict = {}
        for f in final_list:
            final_ori_dict[f] = list(set(ori_dict[f]))

        # 输出最终的列表
        return final_ori_dict

    @staticmethod
    def truncate_text_by_token_count(text: str, max_tokens):
        if text is None:
            text = "a"
        # 使用NLTK库的word_tokenize函数对文本进行令牌化
        tokens = nltk.word_tokenize(text)
        logger.info(len(tokens))
        if len(tokens) > max_tokens:
            text_list = []
            t = 0
            while t < len(tokens):
                if len(tokens) > t + max_tokens:
                    truncated_tokens = tokens[t:max_tokens]  # 如果令牌数量超过目标数量，则截取部分令牌
                else:
                    truncated_tokens = tokens[t:]  # 如果令牌数量超过目标数量，则截取部分令牌

                truncated_text = ' '.join(truncated_tokens)  # 将截取后的令牌重新组合成文本
                text_list.append(truncated_text)
                t = t + max_tokens
            return text_list
        else:
            return [text]  # 如果令牌数量未超过目标数量，则返回原始文本

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

    async def search_youtube_video_of_pre_concept(self, keyword: str, max_results: int = 3):
        prompt = PRE_CONCEPT_SEARCH.format(topic=keyword)
        k_result = await self.llm.aask(prompt)

        # 返回一个字典
        results = YoutubeSearch(k_result, max_results=max_results).to_dict()

        return results

    async def knowledge_collect(self, keyword: str, video_id: str, context: str):
        prompt = KNOWLEDGE_TRANSFER.format(context=context)

        knowledge = await self.llm.aask(prompt)

        logger.info(knowledge)

        self.save_into_json(knowledge, keyword, video_id)

    async def current_video_info(self, video_id: str):
        srt = self.download_video_srt(video_id)
        context = self.arrange_srt_into_text(srt)
        signs = self.sign_collect(context)
        goals = await self.goal_collect(context)

        return signs, goals

    async def goal_collect(self, context: str):
        prompt = GOAL_COLLECT.format(context=context)

        goals_str = await self.llm.aask(prompt) + "\n"

        goals = re.findall(r'- (.*)\n', goals_str)

        r = 0
        while goals is None:
            goals_str = await self.llm.aask(prompt)
            goals = re.findall(r'- (.*)\n', goals_str)
            r = r + 1
            if r > 4:
                logger.info("Fail to collect goals")
                return None

        return goals

    def sign_collect(self, context: str):
        if context is not None:
            kb = KeyBERT("Models/MiniLM-L6-v2")
            signs_list = kb.extract_keywords(
                context,
                keyphrase_ngram_range=(1, 3),
                use_maxsum=True,
                nr_candidates=20,
                diversity=0.9,
                top_n=15)

            signs = [item[0] for item in signs_list]

            return signs

        return

    async def concept_collect(self, topic: str, contexts: [str], video_id: str):
        summarys = ""
        for context in contexts:
            s_prompt = SUMMARY_COLLECT.format(topic=topic, context=context)

            summary = await self.llm.aask(s_prompt)
            summarys = summarys + summary + "\n"

        # concepts = []
        c_prompt = CONCEPT_COLLECT.format(topic=topic, summary=summarys)

        concepts_str = await self.llm.aask(c_prompt) + "\n"

        concepts_list = re.findall(r'- (.*)\n', concepts_str)
        concepts = {}
        for c in concepts_list:
            concepts[c] = [video_id]

        # r = 0
        # while concepts is None:
        #     concepts_str = await self.llm.aask(prompt)
        #     concepts = re.findall(r'- (.*)\n', concepts_str)
        #     r = r + 1
        #     if r > 4:
        #         logger.info("Fail to collect goals")
        #         return None

        time.sleep(20)

        return concepts

    async def collect_video_concept(self, keyword: str, max_results: int = 4, max_tokens: int = 11499):
        search_video_match = {}
        video = self.search_youtube_video(keyword, max_results=max_results)
        p_video = await self.search_youtube_video_of_pre_concept(keyword, max_results=max_results)

        video.extend(p_video)

        for v in video:
            search_video_match[v['id']] = v['title']

        cs = []
        final_dict = {}
        for v in video:
            srt = self.download_video_srt(video_id=v['id'])
            srt_text = self.arrange_srt_into_text(srt)
            srt_text = self.truncate_text_by_token_count(srt_text, max_tokens)
            cs.append(await self.concept_collect(keyword, srt_text, v['id']))
            if len(cs) == 1:
                final_dict = cs[0]
            else:
                final_dict = self.dict_merge(final_dict, cs[len(cs) - 1])

        return final_dict, search_video_match

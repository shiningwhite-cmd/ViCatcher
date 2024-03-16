import asyncio
import os
import threading
import queue
import json

import time

from metagpt.roles.researcher import RESEARCH_PATH
from Role.Researcher import Researcher
from Role.Extractor import Extractor
from Role.WikiResearcher import WikiResearcher
from Module.Intermediary import Intermediary
from metagpt.team import Team
from metagpt.logs import logger


LECTURE_BASE_BACKGROUND = """## BACKGROUND
You are an AI assistant, and your purpose is to learn the ongoing lecture \
and acquire knowledge. This is a lecture about {topic}, and the main context of \
this lecture is shown in the "MAIN CONTEXT" section.

## MAIN CONTEXT
{context}
"""

USER_BASE_BACKGROUND = """## BACKGROUND
You are an AI assistant, and your purpose is to help the user learn the interesting knowledge. \
The user's primary job is {job}, and the specialized areas of interest for users is shown in the \
"AREAS OF INTEREST" section.

## AREAS OF INTEREST
{interest}
"""


def is_valid_json(json_str: str):
    try:
        json_list = json.loads(json_str)
    except ValueError as e:
        return False
    return json_list


class Translator:
    im: Intermediary = None
    extractor = None
    wiki_researcher = None
    keywords = []

    def __init__(self, im: Intermediary = None):
        super().__init__()
        self.im = im

        self.extractor = Extractor(language="zh-cn")
        self.wiki_researcher = WikiResearcher(status="Senior Product Manager", language="zh-cn")

    def keywords_pop_in(self, keyword_list):
        if keyword_list is not None:
            for keyword in keyword_list:
                self.keywords.append(keyword)

    def keywords_pop_out(self):
        if self.keywords:
            return self.keywords.pop()

    def keywords_is_not_none(self):
        if self.keywords:
            return True
        return False

    async def run(self):
        """"""
        while True:
            idea = self.im.get_queue()
            logger.info(idea)

            if idea is not None:
                et_repeat_time = 0
                et_rsp = await self.extractor.run(idea)
                keyword_list = is_valid_json(et_rsp.content)

                while keyword_list is None:
                    et_rsp = await self.extractor.run(idea)
                    keyword_list = is_valid_json(et_rsp.content)

                    et_repeat_time = et_repeat_time + 1
                    if et_repeat_time > 4:
                        break

                # 测试关键词是否合适

                if keyword_list is not None:
                    self.keywords_pop_in(keyword_list)

                continue

            if self.keywords_is_not_none():
                kw = self.keywords_pop_out()

                wr_rsp = await self.wiki_researcher.run(kw)
                knowledge = wr_rsp.content

                logger.info(knowledge)

                continue

            time.sleep(5)

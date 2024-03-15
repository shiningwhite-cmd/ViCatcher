#!/usr/bin/env python
"""
@Modified By: sw, 2024/02/29, use Google api as search engine and add searching sites restriction.
"""

from __future__ import annotations

import asyncio
import requests
import wikipediaapi

import time

from metagpt.actions import Action
from metagpt.config import CONFIG
from metagpt.llm import LLM
from metagpt.logs import logger
from metagpt.provider.base_llm import BaseLLM
from metagpt.tools.search_engine import SearchEngine
from metagpt.tools.web_browser_engine import WebBrowserEngine, WebBrowserEngineType
from metagpt.utils.common import OutputParser
from metagpt.utils.text import generate_prompt_chunk, reduce_message_length
from metagpt.tools import SearchEngineType

WIKI_SEARCH_AND_SUMMARIZE_PROMPT = """### Requirements
1. Summarize the text in the "Reference Information" section into a concise introduction about {topic}.
2. If the information in "Reference Information" section is insufficient, you should add more additional information \
in the introduction.
3. The introduction should be as concise as possible, no more than 100 words.

### Reference Information
{content}

### Introduction
The introduction is:
"""

WITHOUT_WIKI_PROMPT = """### Requirements
1. Generate a concise introduction about {topic}.
3. The introduction should be as concise as possible, no more than 100 words.

### Introduction
The introduction is:
"""

class WikiSearchAndSummarize(Action):
    """Action class to search articles and summarize,"""

    def search_wikipedia(self, query: str):
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query
        }
        response = requests.get(url, params=params)
        data = response.json()

        titlelist = []
        for result in data['query']['search']:
            titlelist.append(result['title'])
            break

        return titlelist

    def get_wikipedia_page_summary(self, title: str) -> str:
        wiki = wikipediaapi.Wikipedia('aa (name@email.com', 'en')

        page = wiki.page(title)
        return wiki.extracts(page)

    async def run(self, topic: str, query: str) -> str:
        page_list = self.search_wikipedia(query)
        page_summary = ""

        for page_title in page_list:
            page_summary = self.get_wikipedia_page_summary(page_title)
            break

        if page_summary != "":
            prompt = WIKI_SEARCH_AND_SUMMARIZE_PROMPT.format(topic=topic, content=page_summary)
        else:
            prompt = WITHOUT_WIKI_PROMPT.format(topic=topic)

        return await self._aask(prompt)

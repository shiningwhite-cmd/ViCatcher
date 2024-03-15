#!/usr/bin/env python
"""
@Modified By: sw, 2024/03/14, use Google api as search engine and add searching sites restriction.
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

RENEW_BASE_PROMPT = """## REQUIREMENT
You should read the context of current lecture, and renew the background message of this lecture. \
The context of lecture will be shown in "CONTEXT" section, and the primary background message is shown in \
"BACKGROUND" section. \

## CONTEXT
{context}

## BACKGROUND
{background}

## 
"""


class LectureBackgroundRenew(Action):
    async def run(
            self,
            lecture_bg: str,
            lecture_ct: str
    ):
        prompt = RENEW_BASE_PROMPT.format(context=lecture_bg, background=lecture_bg)

        rsp = await self._aask(prompt)

        return rsp


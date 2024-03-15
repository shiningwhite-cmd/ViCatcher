#!/usr/bin/env python
"""
@Modified By: sw, 2024/03/02, new actions file.
"""

from __future__ import annotations

import asyncio
from typing import Callable, Optional, Union

import json

import time

from metagpt.actions import Action
from metagpt.logs import logger


EXTRACTOR_BASE_SYSTEM = """You are an AI keyword extractor. Your sole purpose is to extract the proper nouns \
and the words which are more difficult to understand from the given text."""

EXTRACTOR_PROMPT = """# Requirements
1. The keywords you interested in should be proper nouns or the words which are more difficult to understand.
2. The given text is shown in the "Original Text" section, you should extract less than 2 keywords from the text.
3. "Example" section provides you an example of keyword extraction, you can learn from it.
4. Please respond in the following JSON format: ["keyword1", "keyword2"].

# Example
### Original Text
In this work, we present xxxx, a large language model augmented with tools for knowledge retrieval for mathematical reasoning.
### Result
["large language model", "knowledge retrieval"]

# Original Text
{content}

# Result
your result is (no more than 2 keywords):
"""


class KeywordExtract(Action):
    """Action class to extract keywords from one sentence"""

    name: str = "KeywordExtract"
    context: Optional[str] = None
    desc: str = "Extract keywords from one sentence."

    async def run(
        self,
        content: str,
        system_text: str = EXTRACTOR_BASE_SYSTEM,
    ) -> str:
        """Run the action to conduct research and generate a research report.

        Args:
            topic: The research topic.
            content: The content for research.
            system_text: The system text.

        Returns:
            The generated research report.
        """
        prompt = EXTRACTOR_PROMPT.format(content=content)
        logger.debug(prompt)

        rsp = await self._aask(prompt, [system_text])

        return rsp

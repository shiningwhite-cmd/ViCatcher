#!/usr/bin/env python
"""
@Modified By: sw, 2024/02/29, new role file.
"""

import asyncio
import re

from metagpt.actions import Action
from metagpt.const import RESEARCH_PATH
from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message

from Action.SearchInWiki import WikiSearchAndSummarize


class WikiResearcher(Role):
    name: str = "Mark"
    profile: str = "WikiResearcher"
    goal: str = "Gather information and conduct research from wikipedia"
    constraints: str = "Ensure accuracy and relevance of information"
    language: str = "en-us"
    status: str = "AI Agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions(
            [WikiSearchAndSummarize]
        )
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)
        if self.language not in ("en-us", "zh-cn"):
            logger.warning(f"The language `{self.language}` has not been tested, it may not work.")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        msg = self.rc.memory.get(k=1)[0]
        topic = msg.content

        if isinstance(todo, WikiSearchAndSummarize):
            introduction = await todo.run(topic, topic)
            ret = Message(
                content=introduction, instruct_content=None, role=self.profile, cause_by=todo
            )
        else:
            ret = Message(content="", instruct_content=None, role=self.profile, cause_by=self.rc.todo)

        self.rc.memory.add(ret)
        return ret


if __name__ == "__main__":
    import fire

    async def main(topic: str, language="en-us"):
        role = WikiResearcher(language=language)
        await role.run(topic)

    fire.Fire(main)

#!/usr/bin/env python
"""
@Modified By: sw, 2024/03/02, new role file.
"""

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message

from Action.ExtractKeywords import KeywordExtract


class Extractor(Role):
    name: str = "Johnson"
    profile: str = "Extractor"
    goal: str = "Extract keywords"
    constraints: str = "Ensure accuracy and relevance of information"
    language: str = "en-us"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions(
            [KeywordExtract]
        )
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)
        if self.language not in ("en-us", "zh-cn"):
            logger.warning(f"The language `{self.language}` has not been tested, it may not work.")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        msg = self.rc.memory.get(k=1)[0]
        content = msg.content

        if isinstance(todo, KeywordExtract):
            rsp = await todo.run(content)
            ret = Message(
                content=rsp, role=self.profile, cause_by=todo
            )
        else:
            ret = Message(
                content=content, role=self.profile, cause_by=todo
            )

        self.rc.memory.add(ret)
        return ret

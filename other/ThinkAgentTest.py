import asyncio
import re

from metagpt.actions.action import Action
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message

class SimplePrint(Action):
    """
    Action that print the num inputted
    """
    def __init__(self, name="SimplePrint", input_num:int=0):
        super().__init__(name, input_num)

        self.input_num = input_num

    async def run(self, **kwargs):
        print(str(self.input_num) + "\n")
        return 0

class ThinkAction(Action):
    """
    Action that think
    """

    def __init__(self, name="ThinkAction", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction) -> list:
        PROMPT_TEMPLATE = """
            You are now a number list generator, follow the instruction {instruction} and 
            generate a number list to be printed please.
            
            Please provide the number list for me, strictly following the following requirements:
            1. Answer strictly in the list format like [1,2,3,4]
            2. Do not have extra spaces or line breaks.
            Return the list here:
            """

        prompt = PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt=prompt)
        rsp_match = self.find_in_brackets(rsp)

        try:
            rsp_list = list(map(int, rsp_match[0].split(',')))

            return rsp_list
        except:
            return []

    @staticmethod
    def find_in_brackets(s):
        pattern = r'\[(.*?)\]'
        match = re.findall(pattern, s)
        return match

class Printer(Role):
    """

    """

    def __init__(self, name="Jerry", profile="Printer", goal="Print the number", constraints=""):
        super().__init__(name, profile, goal, constraints)

        self._init_actions([ThinkAction])
        self.num_list = list()

    async def _think(self) -> None:
        """Determine the action"""
        logger.info(self._rc.state)

        if self._rc.todo is None:
            self._set_state(0)
            return

        if self._rc.state + 1 < len(self._states):
            self._set_state(self._rc.state + 1)
        else:
            self._rc.todo = None

    async def _prepare_print(self, num_list:list) -> Message:
        """Add actions"""
        actions = list()

        for num in num_list:
            actions.append(SimplePrint(input_num=num))

        self._init_actions(actions)
        self._rc.todo = None
        return Message(content=str(num_list))

    async def _act(self) -> Message:
        """Action"""
        todo = self._rc.todo

        if type(todo) is ThinkAction :
            msg = self._rc.memory.get(k=1)[0]
            self.goal = msg.content
            resp = await todo.run(instruction=self.goal)
            logger.info(resp)

            return await self._prepare_print(resp)

        resp = await todo.run()
        logger.info(resp)

        return Message(content=resp, role=self.profile)

    async def _react(self) -> Message:
        """"""
        while True:
            await self._think()

            if self._rc.todo is None:
                break
            msg = await self._act()

        return msg


async def main():
    msg = "Print numbers from 4 to 6"
    role = Printer()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)


if __name__ == '__main__':
    asyncio.run(main())
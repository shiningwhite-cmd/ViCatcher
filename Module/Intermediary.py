import asyncio
import os
import threading
import queue

import time


class Intermediary:
    """"""
    text_queue: any = None
    text_queue_len: int = 0
    last_item: str = ""

    def __init__(self):
        super().__init__()

        self.text_queue = queue.Queue()
        self.text_queue_len = 0

        pass

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

    def get_last_item(self) -> str:

        return self.last_item

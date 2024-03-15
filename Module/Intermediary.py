import asyncio
import os
import threading
import queue

import time


class Intermediary:
    """"""
    text_queue: any = None
    text_queue_len: int = 0

    def __init__(self):
        super().__init__()

        self.text_queue = queue.Queue()
        self.text_queue_len = 0

        pass

    def put_queue(self, text: str) -> None:
        """get message from outside and store in queue."""
        self.text_queue.put(text)
        self.text_queue_len = self.text_queue_len + 1

        return

    def get_queue(self):
        """put the message to outside and delete it"""
        if self.text_queue_len > 0:
            self.text_queue_len = self.text_queue_len - 1
            return self.text_queue.get()

        return None

#!/usr/bin/env python
import asyncio
import threading

from Module.AnalyseAudio import RecordAndAnalyseAudio
from Module.TranslateKnowledge import Translator
from Module.Intermediary import Intermediary


def run_event_loop(loop, my_coroutine):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(my_coroutine)


async def main():
    im = Intermediary()
    analysis = RecordAndAnalyseAudio(im=im, record_second=10)
    translator = Translator(im=im)

    # 创建一个事件循环
    loop = asyncio.new_event_loop()

    # 启动线程
    audio_thread = threading.Thread(target=analysis.run)
    translate_thread = threading.Thread(target=run_event_loop, args=(loop, translator.run(),))

    audio_thread.start()
    translate_thread.start()

    # 等待线程结束
    audio_thread.join()
    translate_thread.join()

if __name__ == "__main__":
    asyncio.run(main())

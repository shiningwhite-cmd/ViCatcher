import asyncio
import threading
import gradio as gr
import time

from Module.AnalyseAudio import RecordAndAnalyseAudio
from Module.TranslateKnowledge import Translator
from Module.Intermediary import Intermediary

import numpy as np

im = Intermediary()
analysis = RecordAndAnalyseAudio(im=im, record_second=10)
translator = Translator(im=im)

def run_event_loop(loop, my_coroutine):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(my_coroutine)


async def main():
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


def start_audio_transcribe():
    asyncio.run(main())


def get_audio_text():
    return im.get_last_item()


def get_keyword_text():
    return translator.get_this_keyword(), translator.get_this_knowledge()


def get_knowledge_text():
    return


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    audio_text = gr.Text(label="AudioText")
    with gr.Column(scale=4):
        keyword_text = gr.Text(label="Keyword")
        knowledge_text = gr.Text(label="Knowledge")
    off_switch = gr.Button(value="Turn off Relay")


    def respond(chat_history):
        keyword, knowledge = get_keyword_text()
        chat_history.append((keyword, knowledge))
        # time.sleep(2)
        return chat_history

    def load():
        start_audio_transcribe()
        demo.load(respond, inputs=[chatbot], outputs=[chatbot], every=10)

    off_switch.click(load, inputs=None, outputs=None, api_name="turn_off")
    # demo.load(get_audio_text, inputs=None, outputs=[audio_text], every=1)
    # demo.load(get_keyword_text, inputs=None, outputs=[keyword_text, knowledge_text], every=1)
    # demo.launch(get_audio_text, outputs=text, every=5)



# gr.Interface([demo], live=True).launch()
demo.queue().launch()
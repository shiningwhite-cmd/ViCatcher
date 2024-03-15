import asyncio
import os
import threading
import queue

import time

import pyaudio
import wave
import numpy as np
import speech_recognition as sr
import hanlp
from pycorrector.macbert.macbert_corrector import MacBertCorrector


from Module.Intermediary import Intermediary
from metagpt.logs import logger

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


class RecordAndAnalyseAudio:
    record_second: int = 16
    chunk: int = 1024
    format: any = pyaudio.paInt16
    channels: int = 1
    rate: int = 16000
    audio_quene: any = None
    im: Intermediary = None
    hp: any = None
    corrector: MacBertCorrector = None

    def __init__(self, im: Intermediary = None, record_second: int = 16):
        super().__init__()
        self.record_second = record_second
        self.im = im

        # 初始化pyaudio对象
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        self.hp = hanlp.load(hanlp.pretrained.eos.UD_CTB_EOS_MUL)
        # the model path may be stored in a special file
        self.corrector = MacBertCorrector("Models/macbert4csc-base-chinese")

        self.audio_queue = queue.Queue()

    def record_audio(self) -> None:
        """"""
        # 注意音频数据的格式是字节字符串（bytes string）
        frame = b''
        start_time = time.time()
        logger.info("* recording")

        while True:
            data = self.stream.read(self.chunk)

            frame = frame + data
            this_time = time.time()

            if this_time - start_time >= self.record_second:
                # 转换成为整数数组存储到frame缓冲区中（似乎是不必要的操作）
                # samples = np.frombuffer(frame, dtype=np.int16)

                # 存储到缓冲区
                self.audio_queue.put(frame)

                # 刷新
                frame = b''
                start_time = time.time()

        # logger.info("* done recording")

    def recognize_audio(self):
        recognizer = sr.Recognizer()
        while True:
            # 从缓冲区中读取数据
            audio_data = self.audio_queue.get()
            # audio_npdata = np.frombuffer(audio_data, dtype=np.float32)
            if audio_data is None:
                break

            # 将音频数据转换为字节数组
            # audio_bytes = np.frombuffer(audio_data, dtype=np.int16)

            # 将音频数据转换为AudioData对象
            audio_source = sr.AudioData(audio_data, self.rate, sample_width=2)

            # logger.info(audio_data)

            # 使用 whisper 进行识别
            try:
                # 提前设置好本地模型
                # the path of local model might be transfer to a single file
                text = recognizer.recognize_whisper(audio_source, model="./Models/whisper/small.pt", language='zh')
                # text = self.correct_sentence(text)
                # text = self.split_sentence(text)

                logger.info(f"Recognized text: {text}")
                self.im.put_queue(text)
            except sr.UnknownValueError:
                print("No understand")
            except sr.RequestError as e:
                print(f"Error: {e}")

    def correct_sentence(self, input_str: str) -> str:
        output = self.corrector.correct(input_str)
        return output['target']

    def split_sentence(self, input_str: str) -> str:
        # must be moved to init function
        split_sent = self.hp
        output = split_sent(input_str)
        return '\n'.join(output)

    def write_into_file(self, wave_out_path, data):
        wf = wave.open(wave_out_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
        wf.setframerate(self.rate)

        wf.writeframesraw(data)

        wf.close()

    def run(self):
        # 启动线程
        audio_thread = threading.Thread(target=self.record_audio)
        recognize_thread = threading.Thread(target=self.recognize_audio)

        audio_thread.start()
        recognize_thread.start()

        # 等待线程结束
        audio_thread.join()
        self.audio_queue.put(None)  # 发送结束信号
        recognize_thread.join()

    def end(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


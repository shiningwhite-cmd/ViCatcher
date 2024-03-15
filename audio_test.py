#!/usr/bin/env python
import asyncio
import threading

from Module.AnalyseAudio import RecordAndAnalyseAudio
from Module.Intermediary import Intermediary


async def main():
    im = Intermediary()
    analysis = RecordAndAnalyseAudio(im=im, record_second=10)

    analysis.run()

if __name__ == "__main__":
    asyncio.run(main())

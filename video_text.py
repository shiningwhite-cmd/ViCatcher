import asyncio
from Action.SearchVideo import YoutubeVideoSearch
from metagpt.logs import logger

async def main():
    ys = YoutubeVideoSearch()
    keyword = "streamlit"

    video = ys.search_youtube_video(keyword)
    #
    # print(video)
    #
    srt = ys.download_video_srt(video_id=video[0]['id'])
    #
    # print(ys.arrange_srt_into_text(srt))

    # ys.get_json_list()

    logger.info(ys.sign_collect(ys.arrange_srt_into_text(srt)))

if __name__ == "__main__":
    asyncio.run(main())

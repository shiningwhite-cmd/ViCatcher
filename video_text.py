import asyncio
from Action.SearchVideo import YoutubeVideoSearch

async def main():
    ys = YoutubeVideoSearch()
    keyword = "stanford"

    # video = ys.search_youtube_video(keyword)
    #
    # print(video)
    #
    # srt = ys.download_video_srt(video_id=video[0]['id'])
    #
    # print(ys.arrange_srt_into_text(srt))

    ys.get_json_list()

    # await ys.knowledge_collect(keyword, video[0]['id'], ys.arrange_srt_into_text(srt))

if __name__ == "__main__":
    asyncio.run(main())

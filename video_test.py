import asyncio
from Action.SearchVideo import YoutubeVideoSearch
from metagpt.logs import logger

a="""- Python programming basics
- Variables, data types, and type conversion
- Decision-making with if statements
- Working with strings and lists
- Iteration with for loops and range function
- Understanding tuples"""

b="""- Python basics and syntax
- Variables and data types
- Control structures (if-else statements, loops)
- Functions and modular code
- Object-oriented programming (classes, objects, inheritance)
- File handling
- Exception handling"""




async def main():
    ys = YoutubeVideoSearch()

    video = ys.search_youtube_video("python")
    logger.info(video)
    p_video = await ys.search_youtube_video_of_pre_concept("python")

    video.extend(p_video)
    logger.info(video)
    logger.info(p_video)
    # ys.get_json_list()

    # logger.info(await ys.goal_collect(ys.arrange_srt_into_text(srt)))

if __name__ == "__main__":
    asyncio.run(main())

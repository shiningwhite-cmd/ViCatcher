from __future__ import annotations

from Module.Intermediary import Intermediary
from Action.SearchVideo import YoutubeVideoSearch

from metagpt.logs import logger


class DecipherVideo:
    im = None
    ys = None

    def __init__(self, im: Intermediary = None):
        super().__init__()
        self.im = im
        self.ys = YoutubeVideoSearch()

    def download_video_srt(self, video_id: str) -> any:
        return self.ys.download_video_srt(video_id)

    def arrange_srt_into_text(self, srt):
        return self.ys.arrange_srt_into_text(srt)

    def search_youtube_video(self, keyword: str, max_results: int = 5):
        # 返回一个字典
        return self.ys.search_youtube_video(keyword, max_results=max_results)

    def get_title_from_id(self, video_id: str) -> str:
        return self.ys.get_title_from_id(video_id)

    def save_into_json(self, context: str, file_name: str, video_id: str):
        self.ys.save_into_json(context, file_name, video_id)

    def dict_merge(self, dict1: {}, dict2: {}, similarity: int = 0.6):
        return self.ys.dict_merge(dict1, dict2, similarity)

    def truncate_text_by_token_count(self, text: str, max_tokens):
        return self.ys.truncate_text_by_token_count(text, max_tokens)

    async def current_video_info(self, video_id: str):
        return await self.ys.current_video_info(video_id)

    async def goal_collect(self, context: str):
        return await self.ys.goal_collect(context)

    def sign_collect(self, context: str):
         return self.ys.sign_collect(context)

    async def concept_collect(self, topic: str, contexts: [str], video_id: str):
        return await self.ys.concept_collect(topic, contexts, video_id)

    async def collect_video_concept(self, keyword: str, max_results: int = 5, max_tokens: int = 11499):
        final_dict, search_video_match = await self.ys.collect_video_concept(keyword, max_results, max_tokens)

        logger.info("set!")
        self.im.set_video_info(final_dict, search_video_match)

        return

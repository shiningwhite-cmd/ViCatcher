import asyncio
import threading
import time
import pyautogui

import streamlit as st
from streamlit_extras.badges import badge
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.grid import grid
from streamlit_extras.row import row

from Module.AnalyseAudio import RecordAndAnalyseAudio
from Module.TranslateKnowledge import Translator
from Module.Intermediary import Intermediary
from Module.DecipherVideo import DecipherVideo

from metagpt.logs import logger

if 'Intermediary' not in st.session_state:
    st.session_state.intermediary = Intermediary()

analysis = RecordAndAnalyseAudio(im=st.session_state.intermediary)
translator = Translator(im=st.session_state.intermediary)
ys = DecipherVideo(im=st.session_state.intermediary)

def run_event_loop(loop, my_coroutine):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(my_coroutine)


# 创建一个事件循环
loop = asyncio.new_event_loop()

audio_thread = threading.Thread(target=analysis.run)
translate_thread = threading.Thread(target=run_event_loop, args=(loop, translator.run(),))

threads = []
search_video_match = {}

screen_width, screen_height = pyautogui.size()
youtube_player_width = int(screen_width * 1380 / 2560 - 400)
youtube_player_height = int(youtube_player_width * 2 / 3)

async def main():
    # 启动线程
    audio_thread.start()
    translate_thread.start()

    return


def end():
    # 等待线程结束
    audio_thread.join()
    translate_thread.join()


def start_audio_transcribe():
    asyncio.run(main())


def start_collect_concept(keyword: str, search_video_match: {}):
    c_loop = asyncio.new_event_loop()

    c_thread = threading.Thread(
        target=run_event_loop,
        args=(c_loop, ys.collect_video_concept(keyword=keyword, search_video_match=search_video_match),)
    )
    c_thread.start()


def start_audio_extraction():
    t = threading.Thread(target=start_audio_transcribe)
    threads.append(t)
    t.start()


async def get_current_video_info(video_id: str):
    signs, goals = await ys.current_video_info(video_id)

    if signs and goals:
        sign_t = ""
        goal_t = ""
        for sign in signs:
            sign_t = sign_t + sign + ", "

        i = 1
        for goal in goals:
            goal_t = goal_t + str(i) + ". " + goal + "\n"
            i = i + 1

        return sign_t, goal_t

    return "No signs yet", "No goals yet"


def get_audio_text():
    return st.session_state.intermediary.get_last_item() if st.session_state.intermediary.get_last_item() else "Not Audio Text Yet"


def get_keyword_text():
    ke = translator.get_this_keyword() if translator.get_this_keyword() else "Not Keyword Yet"
    kn = translator.get_this_knowledge() if translator.get_this_knowledge() else "Not Knowledge Yet"

#     text_f = """<div style="background-color: #f0f0f5; border: 2px solid #333; border-radius: 10px; padding: 10px;">
#
# #### {ke}
#
# {kn}
#
# </div>
# """
    text_f = """ **{ke}** 

{kn}
\n
"""

    text = text_f.format(ke=ke, kn=kn)
    return text


def search_youtube(term: str):
    video_results = ys.search_youtube_video(term)

    return video_results


class initial():
    ini_id = "Sb0A9i6d320"

    def get_initial_id(self):
        return self.ini_id

    def set_initial_id(self, id: str):
        self.ini_id = id


ini = initial()


async def multi_video_learning(learning_area):
    mla = learning_area.empty()
    learning_area_container = mla.container()
    # 创建一个文本输入框，用于接收搜索关键词
    search_term = learning_area_container.text_input('Search for youtube videos:')
    start_button = learning_area_container.empty()
    search_result = learning_area_container.empty()
    search_result.write("Searching and Learning...")

    if start_button.button(" :dizzy: Start Search"):
        # start_collect_concept(search_term, search_video_match)
        await ys.collect_video_concept(keyword=search_term)
        st.toast('Learning More Video...', icon='😍')

    while all(st.session_state.intermediary.get_video_info()) is False:
        search_result.write("Click the button overhead")
        time.sleep(5)
        return

    search_result_container = search_result.container()
    search_video_match, concept_dict = st.session_state.intermediary.get_video_info()

    search_result_container.markdown(" **Recommended Video Learning Sequence:** ")
    count_v = 1
    learned_v = []

    v_str = """

    """
    m_str = """ 
    
    """

    for value in concept_dict.values():
        c_v = value[0]
        if c_v in learned_v:
            continue

        if search_video_match[c_v]:
            search_result_container.markdown(str(count_v) + " . " + search_video_match[c_v] + v_str + c_v)
            learned_v.append(c_v)
        else:
            search_result_container.markdown(str(count_v) + " . " + v_str + c_v)
            learned_v.append(c_v)
        count_v = count_v + 1

    search_result_container.markdown(" **Related Concepts:** ")
    for key, value in concept_dict.items():
        result_expender = search_result_container.empty()
        with result_expender.expander(key):
            for c_v in value:
                if search_video_match[c_v]:
                    st.markdown(search_video_match[c_v] + m_str + c_v)
                else:
                    st.markdown(m_str + c_v)


async def single_video_learning(learning_area, youtube_id: str):
    sla = learning_area.empty()
    # knowledge_container = stylable_container(
    #     key="container_with_border",
    #     css_styles="""
    #     {
    #         border: 1px solid rgba(49, 51, 63, 0.2);
    #         border-radius: 0.5rem;
    #         padding: calc(1em - 1px)
    #     }
    #     """,
    # )
    learning_single_container = sla.container()

    sign_container = learning_single_container.empty()
    knowledge_container = learning_single_container.container()
    # text_container = learning_single_container.empty()
    # tick_element = learning_single_container.empty()
    button_container = learning_single_container.empty()

    with button_container:
        k_b = row(2)
        if k_b.button('👾 Start'):
            start_audio_extraction()
            pass
        # k_b.button("Reset", type="primary")

    # with text_container.expander(" **:joy: Recognized Audio is Shown Here** ", expanded=True):
    #     st.markdown(get_audio_text())

    _ = get_audio_text()

    with sign_container.expander(" **:star: Goals of Current Video** ", expanded=True):
        s, g = await get_current_video_info(youtube_id)
        # st.markdown(" **Signs:** " + s)
        # st.markdown(" **Goals:** " + g)

        st.markdown(g)
        pass

    with knowledge_container.expander(" **:cool: Keyword Recognizer is Working** ", expanded=True):
        knowledge_show_area = st.empty()
        for tick in range(1000):
            # tick_element.write(tick)
            knowledge_show_area.markdown(get_keyword_text())
            time.sleep(5)


async def APP():
    # 设置页面布局以开启超宽显示模式
    st.set_page_config(layout="wide")

    initial_id = ini.get_initial_id()

    with st.sidebar:
        st.title("ViCatcher")
        badge(type="github", name="shiningwhite-cmd/ViCatcher")
        await multi_video_learning(st.empty())
        pass

    # 创建两列布局
    col1, col2 = st.columns([4, 2])

    with col1:
        initial_url = "https://www.youtube.com/embed/" + initial_id
        iframe_html = """
            <iframe width="{width}" height="{height}" src="{url}" frameborder="0" allow="accelerometer; autoplay; \
            clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            """
        youtube_url = None

        colored_header(
            label="Youtube Video Player",
            description="",
            color_name="violet-70",
        )

        # sc1, sc2 = st.columns(2)
        # with sc1:
        #     badge(type="pypi", name="streamlit")
        # with sc2:
        #     badge(type="github", name="shiningwhite-cmd/KnowledgeTranslator")

        youtube_player_container = st.empty()
        youtube_input_container = st.container()

        # 更新iframe的src属性以加载新的视频
        html = iframe_html.format(url=youtube_url if youtube_url else initial_url,
                                  width=youtube_player_width,
                                  height=youtube_player_height
                                  )
        youtube_player_container.markdown(html, unsafe_allow_html=True)

        with youtube_input_container.popover(" :sunglasses: Youtube Link"):
            st.markdown(" **:sunglasses: Please Type The Link Here!** ")
            # 创建一个文本输入框, YouTube 视频的 URL
            search_youtube_input = st.empty()
            youtube_id = search_youtube_input.text_input("Youtube ID", initial_id)

            v_b = row(2)

            # 创建一个按钮，当点击时更新iframe的src
            if v_b.button("Search Video", key=100):
                youtube_url = "https://www.youtube.com/embed/" + youtube_id
                st.toast('Searching this video...', icon='😍')

                # 更新iframe的src属性以加载新的视频
                html = iframe_html.format(url=youtube_url if youtube_url else initial_url,
                                          width=youtube_player_width,
                                          height=youtube_player_height
                                          )
                youtube_player_container.markdown(html, unsafe_allow_html=True)

            v_b.link_button("Go to the Link", "https://www.youtube.com/watch?v=" + youtube_id)

        if st.button("Reset", type="primary"):
            st.session_state.intermediary.clear_all_saved_data()
            st.stop()

    with col2:
        colored_header(
            label="Knowledge Extractor",
            description="",
            color_name="red-70",
        )

        Learning_Area = st.empty()
        # 根据选择显示页面
        await single_video_learning(Learning_Area, youtube_id)



    # 刷新整个页面
    # st.experimental_rerun()


if __name__ == "__main__":
    asyncio.run(APP())

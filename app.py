import asyncio
import threading
import time

import streamlit as st
from streamlit_extras.badges import badge
from streamlit_extras.colored_header import colored_header

from Module.AnalyseAudio import RecordAndAnalyseAudio
from Module.TranslateKnowledge import Translator
from Module.Intermediary import Intermediary

im = Intermediary()
analysis = RecordAndAnalyseAudio(im=im, record_second=10)
translator = Translator(im=im)


def run_event_loop(loop, my_coroutine):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(my_coroutine)


# 创建一个事件循环
loop = asyncio.new_event_loop()

audio_thread = threading.Thread(target=analysis.run)
translate_thread = threading.Thread(target=run_event_loop, args=(loop, translator.run(),))

threads = []

async def main():
    # 启动线程
    # audio_thread.start()
    # translate_thread.start()

    return


async def end():
    # 等待线程结束
    audio_thread.join()
    translate_thread.join()


def start_audio_transcribe():
    asyncio.run(main())


def get_audio_text():
    return im.get_last_item() if im.get_last_item() else "Not Audio Text Yet"


def get_keyword_text():
    ke = translator.get_this_keyword() if translator.get_this_keyword() else "Not Keyword Yet"
    kn = translator.get_this_knowledge() if translator.get_this_knowledge() else "Not Knowledge Yet"

    text_f = """<div style="background-color: #f0f0f5; border: 2px solid #333; border-radius: 10px; padding: 10px;">
    
#### {ke}

{kn}

</div>
"""

    text = text_f.format(ke=ke, kn=kn)
    return text



# 设置页面布局以开启超宽显示模式
st.set_page_config(layout="wide")

# 侧边栏
with st.sidebar:
    st.title("Test APP")
    badge(type="pypi", name="streamlit")
    badge(type="github", name="shiningwhite-cmd/KnowledgeTranslator")

# 创建两列布局
col1, col2 = st.columns([3, 2])

with col1:
    initial_id = "pxI0I3NX3K0"
    initial_url = "https://www.youtube.com/embed/" + initial_id
    iframe_html = """
        <iframe width="1080" height="630" src="{url}" frameborder="0" allow="accelerometer; autoplay; \
        clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """
    youtube_url = None

    colored_header(
        label="Youtube Video Player",
        description="",
        color_name="violet-70",
    )

    youtube_player_container = st.container()
    youtube_input_container = st.container()

    with youtube_input_container.popover(" :sunglasses: Youtube Link"):
        st.markdown(" **:sunglasses: Please Type The Link Here!** ")
        # 创建一个文本输入框, YouTube 视频的 URL
        youtube_id = st.text_input("Youtube ID", initial_id)

        s_b, g_b = st.columns(2)

        with s_b:
            # 创建一个按钮，当点击时更新iframe的src
            if st.button("Search Video", key=100):
                youtube_url = "https://www.youtube.com/embed/" + youtube_id
        with g_b:
            st.link_button("Go to the Link", "https://www.youtube.com/watch?v=" + youtube_id)

    # 更新iframe的src属性以加载新的视频
    html = iframe_html.format(url=youtube_url if youtube_url else initial_url)
    # 使用st.components.v1.html将iframe嵌入到Streamlit应用程序中
    st.components.v1.html(html, height=630)


with col2:
    # st.metric("Temperature", "70 °F")
    colored_header(
        label="Knowledge Extractor",
        description="",
        color_name="red-70",
    )
    knowledge_container = st.container()
    # 隔出空行
    st.write("")
    text_container = st.container()
    tick_element = st.empty()
    button_container = st.container()

    c1, c2 = button_container.columns(2)
    with c2:
        st.button("Reset", type="primary")
    with c1:
        if st.button('Say hello'):
            # t = threading.Thread(target=start_audio_transcribe)
            # threads.append(t)
            # t.start()
            pass

    with text_container.expander(" **:joy: Recognized Audio is Shown Here** ", expanded=True):
        st.markdown(get_audio_text())

    markdown_element = knowledge_container.empty()
    for tick in range(1000):
        tick_element.write(tick)
        markdown_element.markdown(get_keyword_text(), unsafe_allow_html=True)
        time.sleep(5)

# 刷新整个页面
# st.experimental_rerun()

end()

# Streamlit Timeline Component Example

import streamlit as st
from streamlit_timeline import timeline

import asyncio
from Action.SearchVideo import YoutubeVideoSearch

ys = YoutubeVideoSearch()
#
srt = ys.download_video_srt(video_id="pxI0I3NX3K0")
#
# print(ys.arrange_srt_into_text(srt))

# ys.get_json_list()


# use full page width
st.set_page_config(page_title="Timeline Example", layout="wide")

# load data
with open('example.json', "r") as f:
    data = f.read()

# render timeline
timeline(data, height=800)

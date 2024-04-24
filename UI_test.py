import streamlit as st

# 假设这是你的Intermediary类
class Intermediary:
    def __init__(self):
        self.value = 0

# 检查st.session_state中是否存在intermediary变量
if 'intermediary' not in st.session_state:
    st.session_state.intermediary = Intermediary()

# 访问和更新intermediary变量
def update_intermediary():
    st.session_state.intermediary.value += 1

# 显示intermediary变量的值
st.write('Intermediary value:', st.session_state.intermediary.value)

# 增加intermediary变量的按钮
st.button('Update Intermediary', on_click=update_intermediary)

st.button('Update Interme')
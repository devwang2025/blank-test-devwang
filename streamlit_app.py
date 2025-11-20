import random
import streamlit as st

st.set_page_config(page_title="주사위 굴리기", page_icon="🎲")

st.title("주사위 굴리기 🎲")
st.write("초등학생도 쉽게 사용할 수 있는 간단한 주사위 굴리기 앱이에요. 버튼을 눌러 주사위 2개를 굴려보세요!")

if 'die1' not in st.session_state:
    st.session_state.die1 = 1
if 'die2' not in st.session_state:
    st.session_state.die2 = 1

# 유니코드 주사위 문자 (⚀ ~ ⚅)
DIE_FACES = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']

def roll():
    st.session_state.die1 = random.randint(1, 6)
    st.session_state.die2 = random.randint(1, 6)


st.button("주사위 굴리기! 🎲", on_click=roll)

# 결과를 두 칸으로 보여줍니다
col1, col2 = st.columns(2)
with col1:
    face1 = DIE_FACES[st.session_state.die1 - 1]
    st.markdown(f"<div style='font-size:120px; text-align:center'>{face1}</div>", unsafe_allow_html=True)
    st.write(f"값: **{st.session_state.die1}**")
with col2:
    face2 = DIE_FACES[st.session_state.die2 - 1]
    st.markdown(f"<div style='font-size:120px; text-align:center'>{face2}</div>", unsafe_allow_html=True)
    st.write(f"값: **{st.session_state.die2}**")

total = st.session_state.die1 + st.session_state.die2
st.write(f"합계: **{total}**")

if total == 2:
    st.success("와! 둘 다 1이네 — 아주 희귀해요!")
elif total == 12:
    st.balloons()
    st.success("축하해요! 둘 다 6 — 정말 대박이에요!")
else:
    st.info("다시 굴려볼래요?")

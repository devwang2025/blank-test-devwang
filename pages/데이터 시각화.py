import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

st.set_page_config(page_title="데이터 시각화 예시", page_icon="📊")

st.title("데이터 시각화 예시 페이지 📊")
st.write("임의의 데이터를 만들고 여러 가지 시각화 방법을 간단히 보여주는 예시입니다. 초등학생도 결과를 쉽게 볼 수 있게 구성했어요.")

# Matplotlib 한글 폰트 설정: 프로젝트의 `fonts/NanumGothic-Regular.ttf` 파일을 우선 사용
font_path = Path(__file__).resolve().parents[1] / "fonts" / "NanumGothic-Regular.ttf"
if font_path.exists():
	try:
		fm.fontManager.addfont(str(font_path))
		prop = fm.FontProperties(fname=str(font_path))
		font_name = prop.get_name()
		mpl.rcParams['font.family'] = font_name
		mpl.rcParams['axes.unicode_minus'] = False
	except Exception as e:
		st.warning(f"폰트 로드에 실패했습니다: {e}")
else:
	st.warning(f"한글 폰트 파일을 찾을 수 없습니다: {font_path}")

# 컨트롤
n = st.slider("샘플 수", min_value=100, max_value=5000, value=500, step=100)
seed = st.number_input("랜덤 시드 (같은 데이터를 다시 만들려면 숫자 고정)", value=42, step=1)
generate = st.button("데이터 생성")

if 'df' not in st.session_state:
	st.session_state.df = None

def make_data(n, seed=42):
	rng = np.random.default_rng(seed)
	# 연속형 변수들 (나이, 키, 몸무게, 점수)
	age = rng.normal(loc=10, scale=2.5, size=n).astype(int).clip(6, 15)
	height = (120 + (age - 6) * 5) + rng.normal(0, 6, size=n)
	weight = (25 + (age - 6) * 2) + rng.normal(0, 4, size=n)
	score = rng.normal(loc=75, scale=10, size=n).clip(0, 100)
	# 카테고리 변수
	category = rng.choice(['A', 'B', 'C'], size=n, p=[0.4, 0.35, 0.25])

	df = pd.DataFrame({
		'age': age,
		'height': np.round(height, 1),
		'weight': np.round(weight, 1),
		'score': np.round(score, 1),
		'category': category
	})
	df.index.name = 'id'
	return df

if generate:
	st.session_state.df = make_data(n, seed)

if st.session_state.df is None:
	st.info("왼쪽의 컨트롤에서 샘플 수와 시드를 선택한 뒤 '데이터 생성' 버튼을 눌러주세요.")
	st.stop()

df = st.session_state.df

st.subheader("데이터 미리보기")
st.dataframe(df.head(10))

show_raw = st.checkbox("원시 데이터 전체 보기 (테이블)")
if show_raw:
	st.dataframe(df)

st.subheader("기본 통계 요약")
st.table(df.describe().T[['mean', 'std', 'min', '50%', 'max']].rename(columns={'50%':'median'}))

st.markdown("---")

st.header("다양한 시각화 예시")

# 1) Streamlit 내장 차트: 선/막대/영역
st.subheader("1) Streamlit 간단 차트")
col1, col2, col3 = st.columns(3)
with col1:
	st.write("평균 점수(카테고리별)")
	mean_scores = df.groupby('category')['score'].mean().reindex(['A','B','C'])
	st.bar_chart(mean_scores)
with col2:
	st.write("점수 분포(전체)")
	st.line_chart(df['score'].rolling(10).mean())
with col3:
	st.write("나이별 평균 키")
	age_height = df.groupby('age')['height'].mean()
	st.area_chart(age_height)

st.markdown("---")

# 2) Altair: 산점도와 상자그림
st.subheader("2) Altair 인터랙티브 차트")
scatter = alt.Chart(df.reset_index()).mark_circle(size=60).encode(
	x='height',
	y='weight',
	color='category',
	tooltip=['id', 'age', 'height', 'weight', 'score', 'category']
).interactive()
st.altair_chart(scatter, use_container_width=True)

box = alt.Chart(df.reset_index()).mark_boxplot().encode(
	x='category:N',
	y='score:Q',
	color='category:N'
)
st.altair_chart(box, use_container_width=True)

st.markdown("---")

# 3) Matplotlib: 히스토그램과 상관 행렬
st.subheader("3) Matplotlib 예시")
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(df['age'], bins=range(6, 16), color='#66c2a5', edgecolor='black')
axes[0].set_title('나이 분포')
axes[0].set_xlabel('age')

axes[1].hist(df['score'], bins=20, color='#fc8d62', edgecolor='black')
axes[1].set_title('점수 분포')
axes[1].set_xlabel('score')

st.pyplot(fig)

st.markdown("---")

st.subheader("4) 상관관계 히트맵 (간단)")
corr = df[['age', 'height', 'weight', 'score']].corr()
fig2, ax2 = plt.subplots(figsize=(5, 4))
cax = ax2.matshow(corr, cmap='RdYlBu')
ax2.set_xticks(range(len(corr.columns)))
ax2.set_yticks(range(len(corr.columns)))
ax2.set_xticklabels(corr.columns, rotation=45)
ax2.set_yticklabels(corr.columns)
fig2.colorbar(cax)
st.pyplot(fig2)

st.markdown("---")

st.write("원하시면 이 페이지에 다음 기능을 추가해 드릴게요:")
st.write("- 교사/학생용 간단 설명 추가\n- 랜덤 노이즈/분포 파라미터 조절 컨트롤\n- 그래프 이미지 저장 버튼")


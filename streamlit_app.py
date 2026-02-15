import streamlit as st
import requests
import json

# 1. 환경 설정
WEBAPP_URL = "여기에_배포된_URL_입력"

# 2. UI 레이아웃
st.title("🍎 빼니마니: Health Logger")
user_input = st.text_input("무엇을 하셨나요? (예: 삼겹살 200g 먹었어)")

# 3. 데이터 처리 로직 (Gemini 호출 및 JSON 변환)
if st.button("기록하기"):
    # Gemini API를 통해 자연어를 8개 칼럼 JSON으로 변환하는 프로세스 실행
    # 생성된 JSON 데이터를 requests.post(WEBAPP_URL, data=...) 로 전송
    st.success("데이터가 전송되었습니다.")
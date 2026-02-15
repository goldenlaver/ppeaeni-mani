import streamlit as st
import google.generativeai as genai
import requests
import json
from datetime import datetime

# 1. API 설정
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
APPS_SCRIPT_URL = st.secrets["APPS_SCRIPT_URL"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# 2. UI 구성
st.set_page_config(page_title="빼니마니", page_icon="🩸")
st.title("🩸 빼니마니: Health Dashboard")

# 상단 수치 (예시 데이터, 나중에 시트에서 불러오도록 확장 가능)
col1, col2, col3 = st.columns(3)
col1.metric("현재 체중", "74.6kg")
col2.metric("공복 혈당", "111mg/dL")
col3.metric("활동량", "1.2만보")

st.divider()

# 3. 입력창
user_input = st.text_area("건강 기록을 남겨주세요", placeholder="예: 삼겹살 200g 먹고 1시간 뒤 혈당 130")

if st.button("AI 분석 및 시트 기록"):
    if user_input:
        with st.spinner("AI가 분석 중..."):
            prompt = f"사용자(84년생 남성, 74.6kg)의 입력: '{user_input}'. 이를 [날짜, 시각, 항목, 수치, 식단, 식사 시각, 식후 경과 시간, 비고] 8개 키를 가진 JSON으로 출력해. 비고란에는 대사 관리 조언을 짧게 적어줘."
            response = model.generate_content(prompt)
            # JSON 파싱
            res_text = response.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(res_text)
            
            # 시트 전송
            requests.post(APPS_SCRIPT_URL, json=data)
            st.success("✅ 구글 시트에 기록되었습니다!")
            st.json(data) # AI가 어떻게 분석했는지 보여줌
            st.balloons()

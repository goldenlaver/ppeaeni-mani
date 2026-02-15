import streamlit as st
import google.generativeai as genai
import requests
import json
from datetime import datetime

# 1. API 설정
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    APPS_SCRIPT_URL = st.secrets["APPS_SCRIPT_URL"]
except:
    st.error("Secrets 설정(API 키/URL)을 확인해주세요.")
    st.stop()

# 가장 안정적인 최신 모델 명칭 사용
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. UI 구성
st.set_page_config(page_title="빼니마니", page_icon="🩸")
st.title("🩸 빼니마니 (Ppaeni Mani)")

col1, col2, col3 = st.columns(3)
col1.metric("현재 체중", "74.6kg")
col2.metric("공복 혈당", "111mg/dL")
col3.metric("상태", "근육통 있음")

st.divider()

user_input = st.text_area("기록할 내용을 입력하세요", placeholder="예: 오늘 몸무게 74.2kg")

if st.button("AI 분석 및 기록"):
    if user_input:
        with st.spinner("AI 분석 중..."):
            try:
                # 프롬프트 간소화 (에러 방지)
                prompt = f"사용자(84년생 남성, 74.6kg, 근육통)의 입력: '{user_input}'. [날짜, 시각, 항목, 수치, 식단, 식사 시각, 식후 경과 시간, 비고] 8개 키의 JSON으로만 출력해."
                
                response = model.generate_content(prompt)
                res_text = response.text.strip()
                
                # JSON 정제 로직 강화
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0].strip()
                elif "```" in res_text:
                    res_text = res_text.split("```")[1].strip()
                
                data = json.loads(res_text)
                
                # 구글 시트 전송
                res = requests.post(APPS_SCRIPT_URL, json=data)
                
                if res.status_code == 200:
                    st.success("✅ 구글 시트에 기록되었습니다!")
                    st.balloons()
                    st.json(data)
                else:
                    st.error("시트 전송에 실패했습니다.")
                    
            except Exception as e:
                st.error(f"오류: {e}")
                st.info("모델 명칭 충돌일 수 있습니다. 잠시 후 다시 시도하세요.")

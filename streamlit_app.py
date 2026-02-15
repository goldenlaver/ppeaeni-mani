import streamlit as st
import google.generativeai as genai
import requests
import json
from datetime import datetime

# 1. API 설정 (Secrets에서 안전하게 가져옴)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    APPS_SCRIPT_URL = st.secrets["APPS_SCRIPT_URL"]
except KeyError:
    st.error("Secrets 설정이 필요합니다. (GEMINI_API_KEY, APPS_SCRIPT_URL)")
    st.stop()

# AI 설정 (가장 안정적인 flash 모델 사용)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI 구성 (PWA/Mobile optimized)
st.set_page_config(page_title="빼니마니", page_icon="🩸")
st.title("🩸 빼니마니 (Ppaeni Mani)")

# 사용자 상태 표시 (Summary 데이터 반영)
col1, col2, col3 = st.columns(3)
col1.metric("현재 체중", "74.6kg")
col2.metric("공복 혈당", "111mg/dL")
col3.metric("특이사항", "근육통")

st.divider()

# 3. 입력창
user_input = st.text_area("건강 기록을 남겨주세요", 
                         placeholder="예: 오늘 몸무게 74.2kg / 점심 삼겹살 먹음",
                         height=100)

if st.button("AI 분석 및 기록하기"):
    if user_input:
        with st.spinner("AI 비서가 분석 중입니다..."):
            try:
                # 분석 명령 (사용자 프로필 반영)
                prompt = f"""
                사용자: 1984년생 남성, 74.6kg, 전일 활동으로 근육통 있음.
                입력: "{user_input}"
                위 내용을 분석하여 [날짜, 시각, 항목, 수치, 식단, 식사 시각, 식후 경과 시간, 비고] 8개 키를 가진 JSON으로 출력하라.
                비고란에는 근육통과 혈당 수치를 고려한 짧은 대사 관리 조언을 적어라.
                """
                
                response = model.generate_content(prompt)
                
                # 결과 텍스트 추출 및 정제
                res_text = response.text.strip()
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0].strip()
                
                data = json.loads(res_text)
                
                # 구글 시트로 전송
                res = requests.post(APPS_SCRIPT_URL, json=data)
                
                if res.status_code == 200:
                    st.success("✅ 구글 시트에 기록되었습니다!")
                    st.balloons()
                    st.json(data) # 분석 결과 확인용
                else:
                    st.error(f"시트 전송 실패: {res.text}")
                    
            except Exception as e:
                st.error(f"오류 발생: {e}")
                st.info("API 키 확인 또는 잠시 후 다시 시도해 주세요.")
    else:
        st.warning("내용을 입력해 주세요.")

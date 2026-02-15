import streamlit as st
import google.generativeai as genai
import requests
import json
import pandas as pd # 표를 예쁘게 그리기 위한 도구

# 1. API 설정
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    URL = st.secrets["APPS_SCRIPT_URL"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Secrets 설정을 확인해주세요.")
    st.stop()

st.title("🩸 빼니마니: 기록 영수증")

# 2. 모델 설정 (사용자님이 찾아낸 2.5-flash 강제 지정)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. 입력창
user_input = st.text_area("오늘의 기록을 남기세요", placeholder="예: 삼겹살 200g 먹음 / 몸무게 74.2")

if st.button("AI 분석 및 저장"):
    if user_input:
        with st.spinner("AI 비서가 표를 작성 중입니다..."):
            try:
                prompt = f"사용자(84년생 남성, 74.6kg) 입력: '{user_input}'. [날짜, 시각, 항목, 수치, 식단, 식사 시각, 식후 경과 시간, 비고] 8개 키의 JSON으로만 출력해."
                response = model.generate_content(prompt)
                
                res_text = response.text.strip()
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0].strip()
                
                data = json.loads(res_text)
                
                # 시트 전송
                requests.post(URL, json=data)
                
                st.success("✅ 구글 시트에 기록을 완료했습니다!")
                st.balloons()
                
                # --- 영수증 표 출력부 추가 ---
                st.subheader("📝 기록 영수증")
                df = pd.DataFrame([data]) # 데이터를 표 형태로 변환
                st.table(df) # 화면에 예쁜 표로 출력
                # ---------------------------
                
            except Exception as e:
                st.error(f"실행 오류: {e}")

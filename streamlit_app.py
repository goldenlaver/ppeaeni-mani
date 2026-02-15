import streamlit as st
import google.generativeai as genai
import requests
import json

# 1. API 설정
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    URL = st.secrets["APPS_SCRIPT_URL"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Secrets 설정을 확인해주세요.")
    st.stop()

st.title("🩸 빼니마니: 진단 및 실행 모드")

# 2. 사용 가능한 모델 자동 찾기 (진단 로직)
available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name.replace('models/', ''))
except Exception as e:
    st.error(f"모델 목록을 불러오지 못했습니다: {e}")

# 가장 안정적인 모델 선택 (flash가 없으면 첫 번째 모델 사용)
target_model = 'gemini-1.5-flash' if 'gemini-1.5-flash' in available_models else (available_models[0] if available_models else None)

if target_model:
    st.info(f"✅ 현재 접속 가능한 최적의 모델: **{target_model}**")
    model = genai.GenerativeModel(target_model)
else:
    st.error("사용 가능한 Gemini 모델이 없습니다. API 키를 재확인해주세요.")
    st.stop()

# 3. 입력창 및 로직
user_input = st.text_area("기록을 남겨주세요", placeholder="예: 몸무게 72.2")

if st.button("AI 분석 및 저장"):
    if user_input:
        with st.spinner("분석 중..."):
            try:
                prompt = f"사용자(84년생 남성, 74.6kg) 입력: '{user_input}'. [날짜, 시각, 항목, 수치, 식단, 식사 시각, 식후 경과 시간, 비고] 8개 키의 JSON으로만 출력해."
                response = model.generate_content(prompt)
                
                # 결과 정제
                res_text = response.text.strip()
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0].strip()
                
                data = json.loads(res_text)
                requests.post(URL, json=data)
                
                st.success("✅ 시트에 기록되었습니다!")
                st.balloons()
            except Exception as e:
                st.error(f"실행 오류: {e}")
                st.write("사용 가능한 전체 모델 리스트:", available_models)

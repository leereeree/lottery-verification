import streamlit as st
import random
import hashlib
import json

# 페이지 설정
st.set_page_config(
    page_title="반짝반디의 베뜰 추첨 결과 검증 도구",
    page_icon="🎲",
    layout="centered"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1em;
    }
    .stButton>button:hover {
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        color: #155724;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        color: #721c24;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.title("🎲 추첨 결과 검증 도구")
st.markdown("**Python으로 정확한 검증 (Streamlit)**")

# 사용 방법 안내
st.markdown("""
<div class="info-box">
    <h3 style="color: #667eea; margin-bottom: 0.5rem;">📋 사용 방법</h3>
    <p style="color: #555; line-height: 1.6;">
        Commitment Hash, Timestamp, Nonce를 입력하세요.<br>
        추첨 범위를 지정할 수 있습니다 (선택사항).
    </p>
</div>
""", unsafe_allow_html=True)

# 입력 폼
with st.form("verify_form"):
    commitment_hash = st.text_input(
        "Commitment Hash (추첨 전 공개된 값)",
        placeholder="예: 3b5487bf5365e265...",
        help="추첨 전에 공개된 해시값을 입력하세요"
    )

    timestamp = st.text_input(
        "Timestamp (추첨 전 공개된 값)",
        placeholder="예: 2025-11-18T14:25:15.015655",
        help="추첨 전에 공개된 타임스탬프를 입력하세요"
    )

    nonce = st.text_input(
        "Nonce (추첨 후 공개된 값)",
        placeholder="예: 7ec41d91d6d5c889...",
        help="추첨 후에 공개된 nonce 값을 입력하세요"
    )

    col1, col2 = st.columns(2)
    with col1:
        min_num = st.number_input("최소값 (선택)", min_value=1, value=1, step=1)
    with col2:
        max_num = st.number_input("최대값 (선택)", min_value=1, value=10, step=1)

    submit_button = st.form_submit_button("🔍 검증하기")

# 검증 로직
if submit_button:
    if not commitment_hash or not timestamp or not nonce:
        st.markdown("""
        <div class="error-box">❌ 모든 필수 필드를 입력해주세요.</div>
        """, unsafe_allow_html=True)
    elif min_num > max_num:
        st.markdown("""
        <div class="error-box">❌ 최소값이 최대값보다 클 수 없습니다.</div>
        """, unsafe_allow_html=True)
    else:
        try:
            # 1. 해시 검증
            commitment_data = {
                "nonce": nonce,
                "timestamp": timestamp
            }
            data_string = json.dumps(commitment_data, sort_keys=True)
            calculated_hash = hashlib.sha256(data_string.encode()).hexdigest()

            if calculated_hash != commitment_hash.lower():
                st.markdown(f"""
                <div class="error-box">❌ 검증 실패!

해시값이 일치하지 않습니다.

입력된 Commitment Hash:
{commitment_hash}

계산된 Hash:
{calculated_hash}</div>
                """, unsafe_allow_html=True)
            else:
                # 2. 시드 생성
                seed_string = timestamp + nonce
                seed_hash = hashlib.sha256(seed_string.encode()).hexdigest()
                seed_value = int(seed_hash, 16) % (2**32)

                # 3. 추첨 결과 재현
                random.seed(seed_value)
                result = random.randint(min_num, max_num)

                # 4. 결과 출력
                st.markdown(f"""
                <div class="success-box">✅ 검증 성공!

Commitment Hash (일치):
{commitment_hash}

Timestamp: {timestamp}
Nonce: {nonce}

Seed Value: {seed_value}

추첨 범위: {min_num} ~ {max_num}
🎯 당첨 번호: {result}

✅ 해시 검증 완료! 데이터가 조작되지 않았습니다.</div>
                """, unsafe_allow_html=True)

                # 추가 정보 (접기 가능)
                with st.expander("🔍 자세한 검증 정보"):
                    st.code(f"""
검증 프로세스:
1. Commitment Data 생성:
   {{"nonce": "{nonce}", "timestamp": "{timestamp}"}}

2. JSON 문자열 변환 (정렬):
   {data_string}

3. SHA-256 해싱:
   {calculated_hash}

4. Seed 문자열 생성:
   {timestamp + nonce}

5. Seed Hash 생성:
   {seed_hash}

6. Seed Value 계산:
   {seed_value} = int(seed_hash, 16) % 2^32

7. Python random.seed({seed_value})

8. Python random.randint({min_num}, {max_num}) = {result}
                    """, language="text")

        except ValueError as e:
            st.markdown(f"""
            <div class="error-box">❌ 입력값 오류: {str(e)}

숫자 형식을 확인해주세요.</div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="error-box">❌ 오류 발생: {str(e)}</div>
            """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p>💡 이 도구는 Python의 random 모듈을 사용하여 정확한 검증을 제공합니다.</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

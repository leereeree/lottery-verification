# 🎲 추첨 결과 검증 도구

반짝반디의 베뜰 추첨 결과를 검증하는 웹 애플리케이션입니다.

## 기능

- ✅ Commitment Hash 검증
- ✅ Python random 모듈을 사용한 정확한 난수 재현
- ✅ 투명하고 공정한 추첨 검증

## 사용 방법

1. Commitment Hash (추첨 전 공개된 값) 입력
2. Timestamp (추첨 전 공개된 값) 입력
3. Nonce (추첨 후 공개된 값) 입력
4. 추첨 범위 설정 (선택사항)
5. 검증하기 버튼 클릭

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run verify_drawing_streamlit.py
```

## 기술 스택

- Python 3.10+
- Streamlit
- hashlib (SHA-256)

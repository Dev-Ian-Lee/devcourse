# requests 라이브러리를 사용해 NAVER의 홈페이지를 요청한 뒤 응답 받아보기
import requests

res = requests.get("https://www.naver.com")

# Header 확인
print(res.headers)

# Body 확인
print(res.text[:1000])
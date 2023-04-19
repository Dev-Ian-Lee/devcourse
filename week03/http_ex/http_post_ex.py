import requests

# JSON 형식의 payload를 사용해 POST 요청 전송
payload = {"name": "Lee", "age": 25}

res = requests.post("https://webhook.site/eb936ddc-bc17-482a-88f2-f0dcf6901c0e", payload)

# 상태 코드 확인
print(res.status_code)
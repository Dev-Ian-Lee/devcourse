import requests

res = requests.get("https://www.naver.com/robots.txt")
print(res.text)
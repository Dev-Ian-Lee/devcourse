import requests
from bs4 import BeautifulSoup

res = requests.get("http://www.example.com")

soup = BeautifulSoup(res.text, "html.parser")
print(soup.prettify())

# title 가져오기
print(soup.title)

# head 가져오기
print(soup.head)

# body 가져오기
print(soup.body)

# <h1> 으로 감싸진 요소 하나 찾기
print(soup.find("h1"))

# <p> 로 감싸진 요소들 찾기
print(soup.find_all("p"))

# 태그 이름, 내용 가져오기
h1 = soup.find("h1")
print(h1.name)
print(h1.text)
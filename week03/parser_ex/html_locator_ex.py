import requests
from bs4 import BeautifulSoup

res = requests.get("http://example.python-scraping.com/")

soup = BeautifulSoup(res.text, "html.parser")

# id가 "results"인 div 검색
print(soup.find("div", id = "results"))

# class가 "page-header"인 div 검색
find_result = print(soup.find("div", "page-header"))

# 텍스트 깔끔하게 출력
print(find_result.h1.text.strip())
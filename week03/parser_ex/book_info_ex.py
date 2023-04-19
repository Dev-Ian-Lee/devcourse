import requests
from bs4 import BeautifulSoup

res = requests.get("http://books.toscrape.com/catalogue/category/books/travel_2/index.html")

soup = BeautifulSoup(res.text, "html.parser")

# <h3> 에 해당하는 요소 모두 검색해 제목(Title)만 추출
h3_results = soup.find_all("h3")

for book in h3_results:
    # 속성(Attribute)은 딕셔너리처럼 접근
    print(book.a["title"])
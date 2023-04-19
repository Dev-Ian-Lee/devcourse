import requests
from bs4 import BeautifulSoup
import time

# 스크래핑을 위해 user agent 추가
user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36"}

# Pagination 되어있는 질문 리스트의 제목 모두 추출
# 1page ~ 5page
for i in range(1, 6):
    res = requests.get("https://hashcode.co.kr/?page={}".format(i), user_agent)

    soup = BeautifulSoup(res.text, "html.parser")

    questions = soup.find_all("li", "question-list-item")

    for question in questions:
        # 계층 구조를 연쇄적으로 접근해 질문글의 제목만 추출
        print(question.find("div", "question").find("div", "top").h4.text)

    # 과도한 요청을 방지하기 위해 1초씩 지연
    time.sleep(1)
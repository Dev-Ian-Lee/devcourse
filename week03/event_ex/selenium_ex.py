from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 주어진 명령이 끝나면 드라이버를 종료하도록 with-as 구문 사용
# 크롬 드라이버 객체 생성
with webdriver.Chrome(service = Service(ChromeDriverManager().install())) as driver:
    # 요청 전송
    driver.get("http://example.com")

    # <p> 요소 하나 찾기
    print(driver.find_element(By.TAG_NAME, "p").text)

    # <p> 요소 여러 개 찾기
    for element in driver.find_elements(By.TAG_NAME, "p"):
        print("Text:", element.text)

    # Response의 HTML 문서 확인
    print(driver.page_source)
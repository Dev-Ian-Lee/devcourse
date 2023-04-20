from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

with webdriver.Chrome(service = Service(ChromeDriverManager().install())) as driver:
    driver.get("https://indistreet.com/live?sortOption=startDate%3AASC")

    # 암묵적 기다림(최대 10초)
    driver.implicitly_wait(10)

    # 1초 ~ 10초
    for i in range(1, 11):
        element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div/div[4]/div[1]/div[{}]/div/a/div[2]/p[1]'.format(i))
        print(element.text)

    # 명시적 기다림
    # 타겟으로 명시한 요소를 반환
    # Xpath가 다음과 같은 요소가 존재할 때까지 최대 10초 간 기다림
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div/div[4]/div[1]/div[1]/div/a/div[2]/p[1]')))
    # print(element.text)
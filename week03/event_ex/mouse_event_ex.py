from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.get("https://hashcode.co.kr/")
driver.implicitly_wait(0.5)

# class가 2개 있는 태그 가져오기
button = driver.find_element(By.CLASS_NAME, "nav-link.nav-signin")
ActionChains(driver).click(button).perform()
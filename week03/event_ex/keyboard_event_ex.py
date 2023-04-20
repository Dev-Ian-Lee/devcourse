from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

driver = webdriver.Chrome(service = Service(ChromeDriverManager.install()))
driver.get("https://hashcode.co.kr/")
time.sleep(1)

# 로그인 버튼 찾아서 클릭
button = driver.find_element(By.CLASS_NAME, "nav-link.nav-signin")
ActionChains(driver).click(button).perform()
time.sleep(1)

# 이메일 입력
id_input = driver.find_element(By.ID, "user_email")
ActionChains(driver).send_keys_to_element(id_input, "입력할 email").perform()
time.sleep(1)

# 비밀번호 입력
pw_input = driver.find_element(By.ID, "user_password")
ActionChains(driver).send_keys_to_element(pw_input, "입력할 비밀번호").perform()
time.sleep(1)

# 로그인 버튼 찾아서 클릭
login_button = driver.find_element(By.ID, "btn-sign-in")
ActionChains(driver).click(login_button).perform()
time.sleep(1)
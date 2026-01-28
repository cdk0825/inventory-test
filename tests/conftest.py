import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    
    # 1. 비밀번호 저장 팝업 안 뜨게 설정
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "safebrowsing.enabled": False 
    }
    options.add_experimental_option("prefs", prefs)
    
    # 2. 자동화 제어 정보 표시 제거 및 옵션 설정
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)
    
    # 기본 URL 접속
    driver.get("https://www.saucedemo.com/")
    
    yield driver
    
    # 테스트 종료 후 브라우저 닫기
    driver.quit()
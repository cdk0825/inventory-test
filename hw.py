from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import pytest

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    
    # 1. 비밀번호 저장 팝업 안 뜨게 설정
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        # 핵심: 크롬의 '비밀번호 유출 확인' 및 '세이프 브라우징' 비활성화
        "safebrowsing.enabled": False 
    }
    options.add_experimental_option("prefs", prefs)
    
    # 2. 자동화 제어 정보 표시 제거 및 알림 차단
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()
    
@pytest.fixture
def clean_up(driver):
    # reset_cart(driver)
    print("🧹 장바구니 초기화 (Before Test)")
    
    yield
    reset_cart(driver)
    print("🧹 장바구니 초기화 (After Test)")
    

    
@pytest.mark.parametrize(
    "username, expected_result",
    [
        ("standard_user", True),
        ("locked_out_user", False),
        ("problem_user", True),
        ("performance_glitch_user", True),
        ("error_user", False),
        ("visual_user", True),
    ],
    ids=[
        "정상 사용자",
        "잠긴 사용자",
        "문제 사용자",
        "성능 지연 사용자",
        "에러 사용자",
        "비주얼 사용자",
    ]
)
@pytest.fixture(autouse=True)
def auto_close_popups(driver):
    yield
    driver.execute_script("""
        document.body.style.overflow = 'auto';
        document.querySelectorAll('[role="dialog"]').forEach(e => e.remove());
    """)
    
    
def test_login_parametrize(driver, username, expected_result):
    driver.find_element(By.CSS_SELECTOR, '[data-test="username"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, '[data-test="password"]').send_keys("secret_sauce")
    
    # id.send_keys("standard_user")
    # pw.send_keys("secret_sauce")
    # time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-test="login-button"]').click()
    
    time.sleep(2)
    
    
    if expected_result:
        # 로그인 성공 → inventory 페이지
        assert "inventory.html" in driver.current_url
    else:
        # 로그인 실패 → 에러 메시지 표시
        error_msg = driver.find_element(By.CLASS_NAME, "error-message-container")
        assert error_msg.is_displayed()
    
    
def test_login(driver, clean_up):
    id = driver.find_element(By.CSS_SELECTOR, '[data-test="username"]')
    pw = driver.find_element(By.CSS_SELECTOR, '[data-test="password"]')
    
    id.send_keys("standard_user")
    pw.send_keys("secret_sauce")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-test="login-button"]').click()
    # close_password_popup(driver)
    # force_close_all_popups(driver)
    time.sleep(2)
    
    
    driver.find_element(By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-bike-light"]').click()
    
    
    # data-test="remove-sauce-labs-backpack"
    # data-test="remove-sauce-labs-bike-light"
    
    time.sleep(2)
    clean_up(driver)
    driver.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').click()
    time.sleep(2)
    driver.back()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-test="shopping-cart-link"]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-test="remove-sauce-labs-backpack"]').click()
    driver.back()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-test="remove-sauce-labs-bike-light"]').click()
    time.sleep(2)
    
def reset_cart(driver):
    if "inventory.html" not in driver.current_url:
        return
    wait = WebDriverWait(driver, 5)
    
    wait.until(EC.element_to_be_clickable(
        (By.ID, "react-burger-menu-btn")
    )).click()
    
    wait.until(EC.element_to_be_clickable(
        (By.ID, "reset_sidebar_link")
    )).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(
        (By.ID, "react-burger-cross-btn")
    )).click()
    driver.refresh()
    time.sleep(2)
    # try:
    #     # 1. 사이드바 열기 버튼 클릭
    #     menu_btn = wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
    #     menu_btn.click()
        
    #     # 2. Reset App State 버튼 클릭 (애니메이션 대기를 위해 약간의 유격 필요)
    #     reset_link = wait.until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))) # ID 오타 확인 필수: 보통 하이픈(-)이나 언더바(_) 확인
    #     reset_link.click()
        
    #     # 3. 메뉴 닫기 버튼 클릭
    #     close_btn = wait.until(EC.element_to_be_clickable((By.ID, "react-burger-cross-btn")))
    #     close_btn.click()
        
    #     # 4. (중요) 메뉴가 완전히 닫힐 때까지 대기하거나 페이지 새로고침
    #     # SauceDemo의 경우 Reset을 눌러도 UI 숫자가 즉시 안 바뀔 수 있어 새로고침이 확실합니다.
    #     driver.refresh()
        
    #     time.sleep(3)
        
    # except TimeoutException:
    #     print("❌ Reset Cart 중 타임아웃 발생: 요소를 찾을 수 없거나 클릭할 수 없는 상태입니다.")

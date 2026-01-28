import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def inventory_page(driver):
    return InventoryPage(driver)

# 1. 로그인 파라미터라이즈 테스트
@pytest.mark.parametrize("username, expected_success", [
    ("standard_user", True),
    ("locked_out_user", False),
])
def test_login_scenarios(driver, login_page, username, expected_success):
    login_page.login(username, "secret_sauce")
    
    if expected_success:
        assert "inventory.html" in driver.current_url
    else:
        assert login_page.get_error_status()

# 2. 상품 상세 페이지 진입 및 장바구니 초기화 테스트
def test_product_detail_and_reset(driver, login_page, inventory_page):
    # 로그인
    login_page.login("standard_user", "secret_sauce")

    # 상품 상세 이동
    inventory_page.go_to_product_detail("Sauce Labs Backpack")
    assert "inventory-item.html" in driver.current_url
    
    # 다시 목록으로 (브라우저 뒤로가기 대신 UI 버튼 활용 권장하나 여기선 driver 사용)
    driver.back()

    # 장바구니 담기 및 초기화 (Sidebar Reset 기능 확인)
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    inventory_page.reset_app_state()
    
    # 초기화 후 장바구니 배지가 사라졌는지 확인
    from selenium.common.exceptions import NoSuchElementException
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        
    # 로그아웃
    inventory_page.logout()
    time.sleep(3)
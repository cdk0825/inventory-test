from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.menu_button = (By.ID, "react-burger-menu-btn")
        self.reset_button = (By.ID, "reset_sidebar_link")
        self.close_menu_button = (By.ID, "react-burger-cross-btn")
        self.logout_button = (By.ID, "logout_sidebar_link")

    def add_item_to_cart(self, item_name_id):
        selector = (By.CSS_SELECTOR, f'[data-test="add-to-cart-{item_name_id}"]')
        self.driver.find_element(*selector).click()

    def go_to_product_detail(self, item_name):
        # 텍스트로 상품 클릭
        self.driver.find_element(By.LINK_TEXT, item_name).click()

    def reset_app_state(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.element_to_be_clickable(self.menu_button)).click()
        wait.until(EC.element_to_be_clickable(self.reset_button)).click()
        wait.until(EC.element_to_be_clickable(self.close_menu_button)).click()
        self.driver.refresh()
        
    def logout(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.element_to_be_clickable(self.menu_button)).click()
        wait.until(EC.element_to_be_clickable(self.logout_button)).click()
        
        
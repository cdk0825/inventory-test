from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.CSS_SELECTOR, '[data-test="username"]')
        self.password_field = (By.CSS_SELECTOR, '[data-test="password"]')
        self.login_button = (By.CSS_SELECTOR, '[data-test="login-button"]')
        self.error_message = (By.CLASS_NAME, "error-message-container")

    def login(self, username, password):
        self.driver.find_element(*self.username_field).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_status(self):
        return self.driver.find_element(*self.error_message).is_displayed()
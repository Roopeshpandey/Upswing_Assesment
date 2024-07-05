import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.customlogger import LogGen

logger = LogGen.loggen()

@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_signup_positive(setup):
    logger.info("***************** Test_Signup_Positive_Scenario *********************************")
    driver = setup
    driver.get("https://www.demoblaze.com/")
    logger.info("***************** Browser Launched *********************************")
    driver.find_element(By.ID, "signin2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sign-username"))
    ).send_keys("Admin@8888")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sign-password"))
    ).send_keys("pass@786")
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign up']").click()
    time.sleep(2)  # Allow time for the signup to process

    # Check for signup success or failure
    assert "Sign up successful." in driver.page_source or "This user already exists." in driver.page_source
    logger.info("***************** *********************************")

def test_signup_negative(setup):
    logger.info("***************** Sign up Negative Scenario *********************************")
    driver = setup
    driver.get("https://www.demoblaze.com/")
    logger.info("***************** Browser Launched *********************************")
    driver.find_element(By.ID, "signin2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sign-username"))
    ).send_keys("")  # Empty username
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sign-password"))
    ).send_keys("")  # Empty password
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign up']").click()
    time.sleep(2)  # Allow time for the signup to process

    # Check for error message
    assert "Sign up failed." in driver.page_source
    logger.info("***************** Sign up Failed *********************************")

def test_login_positive(setup):
    driver = setup
    logger.info("***************** Login Positive Test Case *********************************")
    driver.get("https://www.demoblaze.com/")
    logger.info("***************** Browser Launched *********************************")
    driver.find_element(By.ID, "login2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("Admin@8888")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginpassword"))
    ).send_keys("pass@786")
    driver.find_element(By.XPATH, "//button[normalize-space()='Log in']").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )
    assert "Welcome" in driver.page_source
    logger.info("***************** Login Successfully *********************************")

def test_login_negative(setup):
    driver = setup
    logger.info("***************** Login Negative Test Case *********************************")
    driver.get("https://www.demoblaze.com/")
    logger.info("***************** Browser Launched Successfully *********************************")
    driver.find_element(By.ID, "login2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("wronguser")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginpassword"))
    ).send_keys("wrongpassword")
    driver.find_element(By.XPATH, "//button[normalize-space()='Log in']").click()
    time.sleep(2)  # Allow time for the login to process

    assert "User does not exist." in driver.page_source or "Wrong password." in driver.page_source
    logger.info("***************** Login Failed *********************************")

def test_product_browsing(setup):
    driver = setup
    test_login_positive(setup)
    logger.info("***************** Product Browsing Scenario *********************************")
    driver.get("https://www.demoblaze.com/")
    categories = driver.find_elements(By.XPATH, "//a[@class='list-group-item']")
    for category in categories:
        category.click()
        time.sleep(2)  # Allow time for the page to load
#        assert driver.find_elements(By.CSS_SELECTOR, ".card")
    logger.info("***************** Product Browsing Checked *********************************")

def test_add_product_to_cart(setup):
    driver = setup
    test_login_positive(setup)
    logger.info("***************** Add Product to Cart Scenario *********************************")
    laptops_category = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Laptops']"))
    )
    laptops_category.click()
    while True:
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))
            )
            next_button.click()
        except:
            break

    logger.info("***************** Product Last Page *********************************")
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@class='hrefch']"))
    )
    products[-1].click()

    # Click on "Add to cart"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Add to cart']"))
    )
    add_to_cart_button.click()

    WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )
    alert = driver.switch_to.alert
    alert.accept()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Add to cart']"))
    )
    assert "Product added." in driver.page_source
    logger.info("***************** Product Added *********************************")

def test_checkout(setup):
    driver = setup
    logger.info("***************** Checkout Testing Scenario *********************************")

    driver.find_element(By.XPATH, "//a[normalize-space()='Cart']").click()
    driver.find_element(By.XPATH, "//button[normalize-space()='Place Order']").click()
    time.sleep(2)
    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "country").send_keys("Country")
    driver.find_element(By.ID, "city").send_keys("City")
    driver.find_element(By.ID, "card").send_keys("1234567812345678")
    driver.find_element(By.ID, "month").send_keys("12")
    driver.find_element(By.ID, "year").send_keys("2024")
    driver.find_element(By.XPATH, "//button[normalize-space()='Purchase']").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Thank you for your purchase!']"))
    )
    assert "Thank you for your purchase!" in driver.page_source
    logger.info("***************** Checkout Successfully *********************************")

def test_logout(setup):
    driver = setup
    logger.info("***************** Logout Scenario Testing *********************************")

    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout2"))
    )

    WebDriverWait(driver, 10).until_not(
        EC.presence_of_element_located((By.ID, "name"))
    )

    logout_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Log in']"))
    )

    assert "Log in" in driver.page_source
    logger.info("***************** Logout Successfully *********************************")


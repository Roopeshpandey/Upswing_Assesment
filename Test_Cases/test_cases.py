import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Test_Cases.demo import test_login_positive
from utilities.customlogger import LogGen

logger  = LogGen.loggen()

def test_signup_possitive(setup):
    logger.info("***************** Test_Signup_Possitive_Scenerio *********************************")
    driver = setup
    driver.get("https://www.demoblaze.com/")
    logger.info("***************** Browser Launched *********************************")
    driver.find_element(By.ID, "signin2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sign-username"))
    ).send_keys()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sign-password"))
    ).send_keys()
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign up']").click()
    logger.info("***************** Sign up Succesfully *********************************")


def test_signup_negative(setup):
    logger.info("***************** Sign up Negative Scenerio*********************************")
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
    logger.info("***************** Sign up Failed *********************************")


def test_login_possitive(setup):
    driver = setup
    logger.info("***************** Login Possitive test case *********************************")
    driver.get("https://www.demoblaze.com/")
    logger.info("***************** Browser Launched *********************************")
    driver.find_element(By.ID, "login2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("Admin@8888")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginpassword"))
    ).send_keys("pass@786")
    driver.find_element(By.XPATH,"//button[normalize-space()='Log in']").click()
    logger.info("***************** login Succesfully *********************************")



def test_login_negative(setup, username, password):
    driver = setup
    logger.info("***************** Login Negative Test Case *********************************")
    driver.get("https://www.demoblaze.com/")
    logger.info("***************** Browser Launched Succesfully *********************************")
    driver.find_element(By.ID, "login2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("Admin@8888")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginpassword"))
    ).send_keys("pass@786")
    driver.find_element(By.XPATH,"//button[normalize-space()='Log in']").click()
    logger.info("***************** Login Failed *********************************")


def test_product_browsing(setup):
    driver = setup
    test_login_positive(setup)
    logger.info("***************** Product Browsing Scenario *********************************")

    categories = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@id='itemc']"))
    )

    for category in categories:
        category_text = category.text  # Store the category text for logging purposes
        category.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='card h-100']"))
        )

        logger.info(f"***************** Browsing category: {category_text} *********************************")

    logger.info("***************** Product Browsing checked *********************************")


def test_add_product_to_cart(setup):
    driver = setup
    logger.info("***************** Add Product to cart Scenerio *********************************")
    time.sleep(2)
    driver.find_element(By.ID, "//a[normalize-space()='Laptops']").click()
    while True:
        try:
            driver.find_element(By.LINK_TEXT, "Next").click()
            time.sleep(1)
        except:
            break
    logger.info("***************** product last page *********************************")
    products = driver.find_elements(By.XPATH, "//a[@class='hrefch']")
    products[-1].find_element(By.XPATH, "//a[normalize-space()='Add to cart']").click()
    WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)
    assert "Product added." in driver.page_source
    logger.info("***************** Prodcut added  *********************************")


def test_checkout(setup):
    driver = setup
    logger.info("***************** Checkout Testing Scenerio *********************************")

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
    driver.find_element(By.XPATH,"//button[normalize-space()='OK']").click()
    time.sleep(2)
    logger.info("***************** Checkout Succesfully *********************************")

def test_logout(setup):
    driver = setup
    logger.info("***************** Logout Scenario Testing *********************************")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout2"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login2"))
    )
    logger.info("***************** Logout Successfully *********************************")
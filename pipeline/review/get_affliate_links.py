from selenium.webdriver.common.keys import Keys
import time

def get_affiliate_link(webdriver, prod_name):
    # Open the page up
    if webdriver.title != "Amazon.in Associates Central - Home":
        webdriver.get("https://affiliate-program.amazon.in/home")
        time.sleep(25)
    webdriver.find_element_by_id("ac-quicklink-search-product-field").send_keys(prod_name, Keys.ENTER)
    time.sleep(5)
    # Wait for the first link in the list
    webdriver.find_elements_by_class_name("getcode-button")[1].click()
    time.sleep(5)

    return webdriver.find_element_by_tag_name("textarea").get_attribute("value")

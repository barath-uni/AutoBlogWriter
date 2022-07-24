from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from read_links import *
from get_affliate_links import *
from keywordripper import *
user = ""
pwd = ""
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())


def main():
    driver.get("https://www.amazon.in/")
    assert "Amazon" in driver.title
    # Loop through each keyword and enter it in the reader method
    enter_keyword(driver, ["air cooler", "symphony air cooler"])
    # get_affiliate_link(driver, "Sunding SD 548 B 14 Function Waterproof Bicycle Computer Odometer Speedometer")
    tearDown()


def tearDown():
    driver.close()


if __name__ == "__main__":
    main()

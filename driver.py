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
    enter_keyword(driver, ["silent air cooler", "tower air cooler", "portable air coolers", "window air cooler", "mini air cooler", "desert air cooler"])  
    #  "air coolers dyson",
    #  "Bajaj air coolers", "Usha air coolers", "Havells air coolers", "Hindware air coolers", "KenStar air coolers", "artic air coolers"
    # "portable air coolers" "window air cooler", "mini air cooler", "desert air cooler"
    # get_affiliate_link(driver, "Sunding SD 548 B 14 Function Waterproof Bicycle Computer Odometer Speedometer")
    # "silent air cooler" "tower air cooler", 
    tearDown()


def tearDown():
    driver.close()


if __name__ == "__main__":
    main()

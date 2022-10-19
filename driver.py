from numpy import var
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from read_links import *
from get_affliate_links import *
from keywordripper import *
from gpt_content_writer import write_an_article
user = ""
pwd = ""
from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())


def main():
    # driver.get("https://www.amazon.in/")
    # assert "Amazon" in driver.title
    # Loop through each keyword and enter it in the reader method
    # "window air cooler", "mini air cooler", "air coolers dyson"
    # enter_keyword(driver, ["portable air coolers"])
    # "tower air cooler", "window air cooler", "air coolers dyson"  
    # "silent air cooler", "tower air cooler", "window air cooler", "mini air cooler"
    #  "air coolers dyson",
    #  "Bajaj air coolers", "Usha air coolers", "Havells air coolers", "Hindware air coolers", "KenStar air coolers", "artic air coolers"
    # "portable air coolers" "window air cooler", "mini air cooler", "desert air cooler"
    # get_affiliate_link(driver, "Sunding SD 548 B 14 Function Waterproof Bicycle Computer Odometer Speedometer")
    # "silent air cooler" "tower air cooler", 
    # tearDown()
    # Get GPT Content
    start_time=time.time()
    file_path = write_an_article(title="portable air coolers", variations=1)
    write_gpt_content_to_file("portable air cooler, realistic, with control panel",file_path)
    print(f"IT TOOK IN TOTAL = {time.time()-start_time}")
    
def tearDown(): 
    driver.close()


if __name__ == "__main__":
    main()

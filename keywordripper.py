from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from store_file import *
from get_affliate_links import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def enter_keyword2(webdriver, input_keyword_lines):

    search_bar = webdriver.find_element_by_id("twotabsearchtextbox")
    # Enter value
    search_bar.send_keys(input_keyword_lines[0], Keys.ENTER)
    avg_reviews = webdriver.find_element_by_id("p_72/1318477031")
    avg_reviews.click()
    list_of_values = [title for title in WebDriverWait(webdriver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'a-size-base-plus')))]
    print("BEFORE LIST OF VALUES")
    # Multi select the links and store it in an array
    print("LIST OF VALUES")
    list_of_links = []
    print("AFTER LIST OF VALUES")
    for links in list_of_values[:7]:
        list_of_links.append(links.find_element_by_xpath('..').get_attribute("href"))
    if list_of_links is []:
        SystemExit("List of links is empty")
    count = 0
    store_resp = list()
    link = list_of_links[0]
    while True:
        print("IN LOOP")
        resp = rip_links(webdriver, link)
        count += 1
        print(count)
        if resp:
            store_resp.append(resp['val'])
        #     Better to write to a file here
            with open("resp.txt", 'a') as file:
                file.writelines(resp['val'])
            link = resp['link']
        else:
            print("Turned out to be an error")
        if count > 100:
            print("SOMETHIN")
            break
    # If not parse these links and grab all the reviews
import time


def rip_links(webdriver, link):

   return_text = dict()
   try:
        print(link)
        webdriver.get(link)
        return_text["val"] = webdriver.find_element_by_id("productTitle").text
        print(return_text)
        # Get the link for the next click
        print("NEFPRE")
        # #anonCarousel1 > ol
        webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")

        ret_val = WebDriverWait(webdriver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#sp_detail_B0B34WXZ5L > a')))
        print("RET VALLLLLLLLLL")
        print(ret_val)
        for linker in ret_val:
            print(linker.get_attribute("href"))
        return_text['link'] = ret_val[0].get_attribute("href")
        return return_text
   except Exception as e:
       print(f"Exception - {e}")

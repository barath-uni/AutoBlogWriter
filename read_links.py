from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from store_file import *
from get_affliate_links import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def enter_keyword(webdriver, input_keyword_lines):

    for input_word in input_keyword_lines:
        print("-----------------------------------------")
        print(f"CURRENTLY FETCHING FOR THE KEYWORD = {input_word}")
        print("-----------------------------------------")
        search_bar = webdriver.find_element(By.ID, "twotabsearchtextbox")
        # Enter value
        search_bar.send_keys(input_word, Keys.ENTER)

        avg_reviews = webdriver.find_element(By.ID, "p_72/1318477031")
        avg_reviews.click()
        webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(3)
        # Change between a-size-medium and a-size-base-plus
        list_of_values = [title for title in WebDriverWait(webdriver, 50).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'a-size-medium')))]
        print("BEFORE LIST OF VALUES")
        # Multi select the links and store it in an array
        print("LIST OF VALUES")
        print(list_of_values)
        list_of_links = []
        print("AFTER LIST OF VALUES")
        for links in list_of_values:
            list_of_links.append(links.find_element(By.XPATH, '..').get_attribute("href"))
        if list_of_links is []:
            SystemExit("List of links is empty")
        print("LIST OF LINKS")
        print(list_of_links)
        while True:
            output = grab_all_reviews(webdriver, list_of_links)
            if output:
                print("OUTPUT RECEIVED. INFINITYYYYYYYYYYY")
                break
        # If not parse these links and grab all the reviews
        write_links_to_file(output, input_word)


def grab_all_reviews(webdriver, list_of_links):

    list_of_reviews = []
    for link in list_of_links:
        review_text_temp = {}

        try:
            link_review_text = ""
            webdriver.get(link)
            review_text_temp["title"] = webdriver.find_element(By.ID, "productTitle").text
            review_text_temp["link"] = link
            webdriver.find_element(By.CSS_SELECTOR, "a[data-hook='see-all-reviews-link-foot']").click()
            # Get the actual review content
            review_text_container = [title for title in WebDriverWait(webdriver, 50).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'review-text-content')))]
            print(review_text_container)
            for review_class_holder in review_text_container:
                review_text = review_class_holder.find_element(By.TAG_NAME, 'span').text
                if len(review_text.split()) > 20:
                    link_review_text += review_text
            print(len(link_review_text))
            review_text_temp["reviews"] = link_review_text
            # review_text_temp["aff_link"] = get_affiliate_link(webdriver, review_text_temp["title"])
            list_of_reviews.append(review_text_temp)

        except Exception as e:
            print(f"No Reviews found! Skip this product - {e}")
    return list_of_reviews

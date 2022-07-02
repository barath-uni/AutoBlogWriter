from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from store_file import *
from get_affliate_links import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def enter_keyword(webdriver, input_keyword_lines):

    search_bar = webdriver.find_element_by_id("twotabsearchtextbox")
    # Enter value
    search_bar.send_keys(input_keyword_lines[1], Keys.ENTER)

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

    while True:
        output = grab_all_reviews(webdriver, list_of_links)
        if output:
            print("OUTPUT RECEIVED. INFINITYYYYYYYYYYY")
            break
    # If not parse these links and grab all the reviews
    return write_links_to_file(output, input_keyword_lines[1])


def grab_all_reviews(webdriver, list_of_links):

    list_of_reviews = []
    for link in list_of_links:
        review_text_temp = {}

        try:
            link_review_text = ""
            webdriver.get(link)
            review_text_temp["title"] = webdriver.find_element_by_id("productTitle").text
            review_text_temp["link"] = link
            webdriver.find_element_by_css_selector("a[data-hook='see-all-reviews-link-foot']").click()
            # Get the actual review content
            review_text_container = [title for title in WebDriverWait(webdriver, 50).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'review-text-content')))]
            print(review_text_container)
            for review_class_holder in review_text_container:
                review_text = review_class_holder.find_element_by_tag_name('span').text
                if len(review_text.split()) > 20:
                    link_review_text += review_text
            print(len(link_review_text))
            review_text_temp["reviews"] = link_review_text
            # review_text_temp["aff_link"] = get_affiliate_link(webdriver, review_text_temp["title"])
            list_of_reviews.append(review_text_temp)

        except Exception as e:
            print(f"No Reviews found! Skip this product - {e}")
    return list_of_reviews

from re import T
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from store_file import *
from get_affliate_links import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import people_also_ask
import json

def enter_keyword(webdriver, input_keyword_lines):
    # webdriver.get("https://www.amazon.in/product-reviews/B083788D2Q/ref=acr_dp_hist_3?ie=UTF8&filterByStar=three_star&reviewerType=all_reviews#reviews-filter-bar")
    
    # get_all_review_containers(webdriver)

    for input_word in input_keyword_lines:
        start_time = time.time()
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
        list_of_values = [title for title in WebDriverWait(webdriver, 5).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'a-size-medium')))]
        print("BEFORE LIST OF VALUES")
        print(list_of_values)
        # Multi select the links and store it in an array
        # print("LIST OF VALUES")
        # print(list_of_values)
        list_of_links = []
        print("AFTER LIST OF VALUES")
        
        for links in list_of_values[1:]:
            link = links.find_element(By.XPATH, '..').get_attribute("href")
            print("LINK")
            print(link)
            list_of_links.append(link)
        if list_of_links is []:
            SystemExit("List of links is empty")
        print("LIST OF LINKS")
        print(list_of_links)
        output = grab_all_reviews(webdriver, list_of_links)
        if output:
            print("OUTPUT RECEIVED. INFINITYYYYYYYYYYY")
            # TODO: Change the paa to get the correct answer
            resp = people_also_ask.get_answer(input_word)
            resp = json.dumps(resp)
            output[0]['questions'] = resp
            write_links_to_file(output, input_word)
        else:
            print("NO OUTPUT RECEIVED, SKIP this product")
        # If not parse these links and grab all the reviews
        print("TOTAL TIME FOR ONE ITERATION=")
        print(time.time()-start_time)
    
def grab_all_reviews(webdriver, list_of_links):

    list_of_reviews = []
    for link in list_of_links:
        print("LINKK")
        print(link)
        review_text_temp = {}

        try:
            link_review_text = ""
            webdriver.get(link)
            review_count = webdriver.find_element(By.CSS_SELECTOR, "#acrCustomerReviewText").text
            review_count = review_count.split(" ")[0].replace(',', '')
            if int(review_count)>1:   
                review_text_temp["title"] = webdriver.find_element(By.ID, "productTitle").text
                print(review_text_temp["title"])
                review_text_temp["link"] = link
                review_text_temp["img_link"] = WebDriverWait(webdriver, 15).until(EC.visibility_of_all_elements_located((By.ID, "landingImage")))[0].get_attribute("src")
                print(review_text_temp["img_link"])
                # #corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole
                # span.a-price:nth-child(2) > span:nth-child(2) > span:nth-child(2)
                review_text_temp["price"] = WebDriverWait(webdriver, 15).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole")))[0].text
                review_text_temp["review_count"] = review_count
                print(review_text_temp["price"])
                webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight/6);")
                try:
                    # #productOverview_feature_div > div > table
                    table_val = WebDriverWait(webdriver, 15).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#productOverview_feature_div > div > table')))
                    # #poExpander > div.a-expander-content.a-expander-partial-collapse-content.a-expander-content-expanded > div > table
                    review_text_temp["table"] = table_val[0].get_attribute('innerHTML')
                    print("TABLEE")
                    print(review_text_temp["table"])
                except Exception as e:
                    print("EXCEPTION WHILE TRYING TO CAPTURE TABLE")
                    print(e)
                    review_text_temp["table"] = "<table></table>"
                try:
                    review_text_temp["description"] = WebDriverWait(webdriver, 15).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#feature-bullets > ul")))[0].text
                except Exception as e:
                    print("WHILE FETCHING DESCRIPTION")
                    print(e)
                    review_text_temp["description"] = "Description empty"
                webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
                webdriver.find_element(By.CSS_SELECTOR, "a[data-hook='see-all-reviews-link-foot']").click()
                WebDriverWait(webdriver, 5).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#histogramTable > tbody > tr:nth-child(2) > td.aok-nowrap > span.a-size-base > a')))[0].click()
                review_text_container = get_all_review_containers(webdriver)
                for review_text in review_text_container:
                    if len(review_text.split()) > 20:
                        link_review_text += review_text.replace('"','')+"."
                print(len(link_review_text))
                # Clean link_review text from b'' and B''
                link_review_text = link_review_text.lower().replace("b''","")
                review_text_temp["reviews"] = link_review_text
                # review_text_temp["aff_link"] = get_affiliate_link(webdriver, review_text_temp["title"])
                list_of_reviews.append(review_text_temp)
            else:
                print("REVIEWS NOT ENOUGH")
        
        except Exception as e:
            print(f"No Reviews found! Skip this product - {e}")
    return list_of_reviews

def get_all_review_containers(webdriver):
    review_text_container = list()
    times = 1
    try:
        while times<10:
            # #customer_review-R1EKLYT8TBJ39Y > div:nth-child(5) > span:nth-child(1)
            # Get the actual review content
            try:
                review_texts = WebDriverWait(webdriver, 5).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span[data-hook='review-body']")))
                if review_texts[0].text not in review_text_container:
                    review_text_container += [title.text for title in review_texts]
            except Exception as e:
                print("STUCK WHILE FETCHING THE DATA")
            
            attempt = 1
            success = False
            while attempt<=3:
                try:
                    next_page = WebDriverWait(webdriver, 5).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'#cm_cr-pagination_bar > ul > li.a-last')))[0]
                    next_page.click()
                    success = True
                except Exception as e:
                    print(e)
                    attempt+= 1
                if success:
                    break
            print("LOOP")
            times += 1
    except Exception as e:
        print("LAST PAGE HIT")
        print(e)
    print("VALUE AT THE END")
    print(review_text_container)
    return review_text_container
# from pipeline.review.read_links import *
# from pipeline.review.get_affliate_links import *
from pipeline.paa.bin import clean_and_generate_summary
# from gptgenerator.gpt_content_writer import write_an_article
user = ""
pwd = ""

# def generate_affiliate_articles(values:list):
#     for value in values:
#         driver = webdriver.Chrome(ChromeDriverManager().install())
#         driver.get("https://www.amazon.in/")
#         assert "Amazon" in driver.title
#         # # Loop through each keyword and enter it in the reader method
#         enter_keyword(driver, [value])
#         # Get GPT Content
#         # start_time=time.time()
#         # file_path = write_an_article(title=value, variations=1)
#         # write_gpt_content_to_file(f"{value}, air cooler with lcd controls, on the floor, photo realistic, 4K HD,near a window, few plants nearby, clean atmosphere",file_path)
#         # print(f"IT TOOK IN TOTAL = {time.time()-start_time}")
#         driver.close()

# def tearDown(): 
#     driver.close()


if __name__ == "__main__":
    csv_val = clean_and_generate_summary.read_csv("home_cooler_8.csv")
    clean_and_generate_summary.store_dict(csv_val)
    # generate_affiliate_articles(["Portable air cooler", "Window air cooler", "Mini air cooler", "Desert Air Cooler", "Silent Air Cooler"])

"""

    For image
"dyson air cooler", 
    ["portable air cooler", "desert air cooler", "dyson air cooler", ""]

"""
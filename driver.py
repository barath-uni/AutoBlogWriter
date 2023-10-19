# from pipeline.review.read_links import *
# from pipeline.review.get_affliate_links import *
# from pipeline.paa.bin import clean_and_generate_summary
# from pipeline.imagegen.stableDiffusionImageGenerator import create_hero_image
# from utils.store_file import hero_image_prompt_builder
from pipeline.imagegen.stableDiffusionImageGenerator import create_hero_image
from utils.store_file import hero_image_prompt_builder
from pipeline.kwresearch import generate_long_tails
from gptgenerator.bin import gpt_blog_write
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

import json
import markdownify
from pathlib import Path

def convert_html_to_markdown(html):
    text = markdownify.markdownify(html, heading_style="ATX")
    return text

def final_touchdown():
    """
    Cleans up the final html and converts it to template ready .md file.
    Can work on its own
    """
    p = Path(r'/home/barath/codespace/blogwriter/AutoBlogWriter/towrite').glob('**/*')
    file_names = [x.stem for x in p if x.is_file()]

    # save to a file
    for file in file_names:
        template_base = \
f"""---
title: GENERATED:"{file}"
description: "If you are looking for a good Tower Air Cooler in India and are confused with multiple options, this article is for you. We look at some of the best air coolers giving bang for the buck and have created a list of all the reliable Tower Air Coolers that you can purchase today."
date: 2022-11-17T14:33:00Z
image: /assets/images/posts/hero/5R92I7_tower_ai.png
categories: ["Tower Air Cooler"]
authors: ["Priyanka sundar"]
tags: ["air cooler", "general"]
draft: true
---
"""
        with open(f'towrite/{file}.html', 'r') as f:
            value = f.read()
            markdown = convert_html_to_markdown(value)
        # Add some additional info here and add the value
        template_base += "\n"+ markdown
        # write to a md file in _output
        with open(f'_output/{file}.md', 'w') as f:
            f.write(template_base)

if __name__ == "__main__":
    # csv_val = clean_and_generate_summary.read_csv("home_cooler_8.csv")
    # clean_and_generate_summary.store_dict(csv_val)
    # generate_affiliate_articles(["Portable air cooler", "Window air cooler", "Mini air cooler", "Desert Air Cooler", "Silent Air Cooler"])
    # file_names = gpt_blog_write.read_and_create_gpt_content()
    # # file_names = ["desiccant_humidifier", "benefits_of_demudifier", "whole_house_dehumidifier", "why_dehumidifier_not_collect_water"]
    # for file in file_names:
    #     with open(f'gpt_output/{file}.json', 'r') as f:
    #         json_dict = json.load(f)
    #         value = gpt_blog_write.convert_json_to_html(json_dict)
    
    #     with open(f'towrite/{file}.html', 'w') as f:
    #         f.write(value)
    # final_touchdown()
    create_hero_image(hero_image_prompt_builder("humidity, mold formation, household, furniture looking moldy"))
#     generate_long_tails.generate_paa_title_answers(
# ["how long do whole house dehumidifiers last",
# "how to check humidity in house",
# "how to measure humidity in home",
# "how to use a dehumidifier",
# "how to protect electronics from humidity",
# "what should i set my dehumidifier at in winter",
# "why can you use calcium chloride to reduce moisture",
# "why do clothes smell musty in closet"])


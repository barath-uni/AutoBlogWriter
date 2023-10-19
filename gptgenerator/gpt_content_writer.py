from asyncore import write
import os
import json
from regex import B
import openai
import re
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

GPT_STORAGE_DIRECTORY = Path("gpt_content_store")

def clean_up_response(string):
    return re.sub(r'[-\|].*', '', string)

def split(s):
    s = re.sub(r'(\d. \n)+', '', s)
    split_val= re.split('\n', s, flags=re.IGNORECASE)
    return "\n".join(split_val)

openai.api_key = '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'

# Works only with GPT3
def generate_heading_for_content(text):
  hook="Create a title for this paragraph"
  response = openai.Completion.create(
  model="text-davinci-002",
  prompt=f"{hook}:\n{text}",
  temperature=0.65,
  max_tokens=50,
  top_p=0.93,
  frequency_penalty=1,
  presence_penalty=1
  )
  value = clean_up_response(response['choices'][0]['text'])
  return value

# Works very well with GPT2 (k, top-p has to be checked)
def generate_long_form_content(text):
  text = "Complete this with more sentences for a blog article:"+"\n"+text
  response = openai.Completion.create(
    engine="text-davinci-002",
      prompt=text,
      temperature=0.6,
      max_tokens=600,
      top_p=0.9,
      frequency_penalty=0.9,
      presence_penalty=0.6
  )
  value = split(response['choices'][0]['text'])
  return value

# Works well with gpt2
def complete_sentences(text, temp=0.7, top_p=1, f_p=0.6, p_p=0.6, max_token=300):
  response = openai.Completion.create(
    engine="text-davinci-003",
      prompt=text,
      temperature=temp,
      max_tokens=max_token,
      top_p=top_p,
      frequency_penalty=f_p,
      presence_penalty=p_p
  )
  value = split(response['choices'][0]['text'])
  return value

# Only with GPT3
def get_text_with_suffix_prefix(text, suffix):
  response = openai.Completion.create(
    engine="text-davinci-002",
      prompt=text,
      suffix=suffix,
      temperature=0.81,
      max_tokens=400,
      top_p=1,
      frequency_penalty=0.96,
      presence_penalty=0.53
  )
  value = split(response['choices'][0]['text'])
  return value

def paraphrase_and_change_tone(text):
  text = f"Complete this in a fun, humorous and personal tone: {text}"
  response = openai.Completion.create(
    engine="text-davinci-003",
      prompt=text,
      temperature=0.7,
      max_tokens=1024,
  )
  value = split(response['choices'][0]['text'])
  return value

# GPT2 does well(Surprisingly)
def convert_question_to_hook(question):
  start_sequence = "\nA:"
  restart_sequence = "\n\nQ: "

  response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"I am a highly intelligent question to introduction conversion bot. If you ask me a question, I will convert it to a introduction hook used for blog articles.\n\nQ: Is cooler cheaper than AC?\nA: Wondering if air coolers are less expensive that an AC?\n\nQ: Who should not use air cooler?\nA: Do you have an air cooler and want to know if it is safe?\n\nQ: How many hours can air cooler work?\nA: Have you thought ,how long can an air cooler run?\n\nQ: Is air cooler cooler than fan?\nA: Do you want to know if an air cooler is better than a fan?\n\nQ: Can we use AC and cooler together?\nA: Have you wondered if you can use an AC and an air cooler together?\n\nQ: Which is best table fan or air cooler?\nA: Trying to decide between a table fan and an air cooler?\n\nQ: How can I make my room cooler without AC?\nA: On a budget and want to know if you can cool down your room temperature without an AC?\n\nQ: Is tower fan and air cooler same?\nA: Not sure if a tower fan and an air cooler are the same thing?\n\nQ: Which cooler is best for closed room?\nA: Are you currently looking for a good air cooler for a closed room?\n\nQ: How can I cool my house without AC and ice?\nA: Are you looking for ways to cool your house without AC or ice?\nQ: {question}\nA:",
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
  )
  value = split(response['choices'][0]['text'])
  return value

def generateBlogTopics(prompt1):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Generate blog topics on: {}. \n \n 1.  ".format(prompt1),
      temperature=0.7,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    value = split(response['choices'][0]['text'])
    # Response has a total tokens to keep track of the total count of items that gets
    return value

def generateBlogSections(prompt1):
    response = openai.Completion.create(
      engine="davinci-instruct-beta-v3",
      prompt="Expand the blog title in to high level blog sections: {} \n\n- Introduction: ".format(prompt1),
      temperature=0.6,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response['choices'][0]['text']

def generate_review(product_description):
    prompt = f"Convert the following product description into a product review with 1000 words or more: {product_description}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
    )

    review = response["choices"][0]["text"]
    print(review)

def blogSectionExpander(prompt1):
    response = openai.Completion.create(
      engine="davinci-instruct-beta-v3",
      prompt="Expand the blog section in to a detailed professional , witty and clever explanation.\n\n {}".format(prompt1),
      temperature=0.7,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response['choices'][0]['text']

def write_an_article(title, variations=1):
  """
  Ideally, we should start with a title (Not keywords, but title) and build an intro + Section + Outro
  What this method does
  1. From title generate blog topics - Possible 5
  2. For each blog topic generate sections - 5 sections on average
  3. For each section build expand
  4. Generate a conclusion for the blog article
  Output -> title + Sections + Outro
  """
  
  blog_topics = generateBlogTopics(title)
  blog_topics = [topic for topic in blog_topics if topic != '']
  assert variations < 4, "Cannot get more than 4 variations at once."\
                          "Will require a lot of GPT hours which we cannot afford"
  blog_topics = blog_topics[:variations]
  print("BLOG TOPICS SO FAR")
  print(blog_topics)
  blog_article_dict = dict()
  # Test this later
  # Use common methods to break the topics into multiple sections
  start_time = time.time()
  for topic in blog_topics:
    print(f"TOPICS = {topic}")
    # Only if length of the topic is greater than 10 characters
    if len(topic) > 10:
      get_sections = split(generateBlogSections(topic))
      get_sections = [section for section in get_sections if section != '']
      print(f"SECTIONS = {get_sections}")
      for section in get_sections:
        expanded_section = blogSectionExpander(section)
        if not blog_article_dict.get(topic, None):
          blog_article_dict[topic]= {section: expanded_section}
        else:
          blog_article_dict[topic][section]= expanded_section
  print(blog_article_dict)
  if Path.exists(GPT_STORAGE_DIRECTORY/f'{title}_content_var_{variations}.json'):
    storage_loc = GPT_STORAGE_DIRECTORY/f'{title}_2_content_var_{variations}.json'
  else:
    storage_loc = GPT_STORAGE_DIRECTORY/f'{title}_content_var_{variations}.json'
  storage_path = Path(storage_loc)  
  # Save to a file so it stays there persistently
  with open(storage_path, 'w') as f:
    json.dump(blog_article_dict, f)
  end_time = time.time() - start_time
  print(f"IT TOOK - {end_time}")
  return storage_path

def scrape_product_page(url):
    # Send a GET request to the given URL and parse the HTML response
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape the product name and description
    product_name = soup.find("span", {"id": "productTitle"}).text
    product_description = soup.find("div", {"id": "feature-bullets"}).text

    # Scrape the user reviews
    reviews = []
    review_elements = soup.find_all("div", {"class": "a-section a-spacing-none review-views celwidget"})
    for review_element in review_elements:
        review_text = review_element.find("span", {"class": "a-size-base review-text"}).text
        reviews.append(review_text)

    # Return the product name, description, and user reviews
    return product_name, product_description, reviews

def scrape_product_page(url):
    # Send a GET request to the given URL and parse the HTML response
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape the product name and description
    product_name = soup.find("span", {"id": "productTitle"}).text
    product_description = soup.find("div", {"id": "feature-bullets"}).text

    # Scrape the user reviews
    reviews = []
    review_elements = soup.find_all("div", {"class": "a-section a-spacing-none review-views celwidget"})
    for review_element in review_elements:
        review_text = review_element.find("span", {"class": "a-size-base review-text"}).text
        reviews.append(review_text)

    # Return the product name, description, and user reviews
    return product_name, product_description, reviews

def generate_product_comparison(product_1, product_2):
    product_1_reviews = '\n'.join(product_1['reviews'])
    product_2_reviews = '\n'.join(product_2['reviews'])
    prompt = f"Write a blog like article with subheadings comparing {product_1['name']} and {product_2['name']} with the following information:\n\n{product_1['name']}:\nProduct description: {product_1['description']}\nUser reviews:\n{product_1_reviews}\n\n{product_2['name']}:\nProduct description: {product_2['description']}\nUser reviews:\n{product_2_reviews}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        temperature=0.7,
    )

    comparison = response["choices"][0]["text"]
    print(comparison)



if __name__ == "__main__":
    # val=generate_heading_for_content('Air coolers do humidify the air, but they also keep it moving so it does not get stale.\n\n They are definitely worth buying if you live in a dry climate, or if you have problems with allergies or asthma.')
    # print(val)
    # val=generate_long_form_content('Air coolers do humidify the air, but they also keep it moving so it does not get stale.\n\n They are definitely worth buying if you live in a dry climate, or if you have problems with allergies or asthma.')
    # print(val)
    # val=generate_heading_for_content('Air coolers do humidify the air, but they also keep it moving so it does not get stale.\n\n They are definitely worth buying if you live in a dry climate, or if you have problems with allergies or asthma.')
    # print(val)

    product_1_url = "https://www.amazon.in/Bajaj-Torque-New-Honeycomb-Technology/dp/B09R3QNGW5/"
    product_1_name, product_1_description, product_1_reviews = scrape_product_page(product_1_url)
    product_1 = {
        "name": product_1_name,
        "description": product_1_description,
        "reviews": product_1_reviews,
    }

    product_2_url = "https://www.amazon.in/Crompton-Greaves-75-Litre-Desert-Cooler/dp/B01DPL9B00/"
    product_2_name, product_2_description, product_2_reviews = scrape_product_page(product_2_url)
    product_2 = {
        "name": product_2_name,
        "description": product_2_description,
        "reviews": product_2_reviews,
    }
    generate_product_comparison(product_1, product_2)
    # first_opening = generateBlogTopics('Tower air cooler for home in india')
    # print(first_opening)
    # second_continuation = generateBlogSections(first_opening[2]+'Benefits of using a tower air cooler in your home in India')
    # print(second_continuation)
    # end_of_blog = blogSectionExpander(second_continuation[3]+'Tower air cooler vs. other cooling methods:')
    # print(end_of_blog)
#   """
#   ['', 'Are you looking for a tower air cooler for your home in India? ', 'If so, you may be wondering which one is the best option for you. ', 'In this blog post, we will compare some of the most popular tower air coolers on the market and help you decide which one is right for you. ', '', 'tower air cooler for home in india', '', 'Which tower air cooler is best for home in india? ']
#   ['', '- Tower air cooler vs. other types of air conditioners: ', '- How a tower air cooler works: ', '- Advantages of using a tower air cooler in your home: ', '- Disadvantages of using a tower air cooler in your home: ', '- Conclusion:']


# A tower air cooler is an ideal way to cool your home during the summer months. Tower air coolers offer many advantages over other cooling methods, such as central air conditioning or window air conditioning units.

# Some of the key advantages of using a tower air cooler in your home include:

# -Tower air coolers are much more affordable than central air conditioning systems.

# -Tower air coolers are much smaller and more compact than central air conditioning systems, making them ideal for homes with limited space.

# -Tower air coolers are very easy to operate and require no installation.

# -Tower air coolers can cool a room much more quickly and effectively than window air conditioning units.

# -Tower air coolers use less energy than central air conditioning systems, making them more energy-efficient.

# If you are looking for a cost-effective, space-saving way to cool your home during the summer months, a tower air
#   """

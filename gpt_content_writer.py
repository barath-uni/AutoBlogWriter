from asyncore import write
import os
import json
from regex import B
import openai
import re
import time
def split(s):
    s = re.sub(r'(\d. \n)+', '', s)
    return re.split('\n', s, flags=re.IGNORECASE)

openai.api_key = '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'


def generateBlogTopics(prompt1):
    response = openai.Completion.create(
      engine="text-davinci-001",
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

def write_an_article(title):
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
  blog_article_dict = dict()
  # Test this later
  # Use common methods to break the topics into multiple sections
  start_time = time.time()
  for topic in blog_topics:
    # Only if length of the topic is greater than 10 characters
    if len(topic) > 10:
      get_sections = split(generateBlogSections(topic))
      for section in get_sections:
        if len(section) > 10:
          expanded_section = blogSectionExpander(section)
          if topic not in blog_article_dict.keys():
            blog_article_dict[topic]= { section: expanded_section}
          else:
            blog_article_dict[topic].update(section, expanded_section)

  # Save to a file so it stays there persistently
  with open('GPT-writer-out.json', 'w') as f:
    json.dump(blog_article_dict, f)
  end_time = time.time() - start_time
  print(f"IT TOOK - {end_time}")

if __name__ == "__main__":
    write_an_article('Tower air cooler for home in india')
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

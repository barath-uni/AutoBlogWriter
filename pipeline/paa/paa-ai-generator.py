# Read CSV
# Sanitize the URL Title
# For each subheading. SH+Paraphrase Text and Use it for Text completion (GPT) (Complete this with 200 more words: + %>% ) and send it
# Generate Image (Stable diffusion 512, 512 Fixed Home air cooler, extra stuff)
# Create _posts (Title-without question-cut to 5 words.html)
# Word count (Metric)
# Publish
import csv
import re
from AutoBlogWriter.utils.format_text import split_text_to_para
from AutoBlogWriter.utils.process_site_and_summarize import read_and_get_wordcount, read_and_summarize

from AutoBlogWriter.gptgenerator.gpt_2_generation import generate_title, generate_content
from AutoBlogWriter.pipeline.paa.paa_cluster import cluster_questions, generate_embeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from AutoBlogWriter.pipeline.imagegen.stableDiffusionImageGenerator import create_hero_image
from AutoBlogWriter.utils.store_file import hero_image_prompt_builder
from AutoBlogWriter.gptgenerator.gpt_content_writer import clean_up_response, convert_question_to_hook, generate_heading_for_content, generate_long_form_content,complete_sentences,  get_text_with_suffix_prefix, paraphrase_and_change_tone
from pathlib import Path
import hashlib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


model = AutoModelForSeq2SeqLM.from_pretrained("ramsrigouthamg/t5-large-paraphraser-diverse-high-quality")
tokenizer = AutoTokenizer.from_pretrained("ramsrigouthamg/t5-large-paraphraser-diverse-high-quality")
import torch
import datetime
import random
import pycountry
import time

def random_conclusion(list=["In Summary", "Closing Thoughts", "Ultimately"]):
    return random.choice(list)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
POST_WRITE_PATH=Path("/home/barath/codespace/coolerssstack/_posts")
SITEMAP_PATH=Path("/home/barath/codespace/coolerssstack/public/sitemap.xml")
url_list = list()

def sanitize(row):
    date_regex = re.compile(r'\d{1,2} \w+ \d{4}')
    # Read the url and see the word count, if it is more than 2000 then don't continue
    word_count = read_and_get_wordcount(row['URL'])
    if word_count > 2000:
        return None
    print(f"THE WORD COUNT FOR {row['URL']} ARTICLE IS", word_count)
    # Don't allow duplicate URL rows, this affects the datasummarizer
    if row['URL'] in url_list:
        return None
    url_list.append(row['URL'])
    found = False
    for key in row:
        for country in pycountry.countries:
            if country.name in row[key]:
                return None
        mo = date_regex.search(row[key])
        if mo:
            return None
        if 'air cool' in row[key].lower():            
            found=True
            break
    if found:
        return row


def paraphrase(text):
    text = "paraphrase: "+text+ " </s>"
    encoding = tokenizer.encode_plus(text,max_length =128, padding=True, return_tensors="pt")
    input_ids,attention_mask  = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    model.eval()
    diverse_beam_outputs = model.generate(
    input_ids=input_ids,attention_mask=attention_mask,
    max_length=128,
    early_stopping=True,
    num_beams=2,
    num_beam_groups = 2,
    num_return_sequences=2,
    diversity_penalty = 0.70)
    print ("\n\n")
    print ("Original: ", text)
    for beam_output in diverse_beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
    print("\n\n")
    print(f"Paraphrased: {sent}")
    return re.sub(r'paraphrasedoutput: ', '', sent)

def read_csv(csv_to_read):
    csv_to_dict = dict()
    with open(csv_to_read, 'r') as file:
        csv_data = csv.DictReader(file)
        # Sanitize
        for row in csv_data:
            row = sanitize(row)
            print(row)
            if row:
                if row['Parent'] in csv_to_dict:
                    csv_to_dict[row['Parent']].append({'subheading': row['\ufeffPAA Title'], 'text': row['Text'], 'URL': row['URL'], 'URL Title': row['URL Title']})
                else:
                    csv_to_dict[row['Parent']] = [{'subheading': row['\ufeffPAA Title'], 'text': row['Text'], 'URL': row['URL'], 'URL Title': row['URL Title']}]
    return csv_to_dict

def clean_up_title(string):
    return re.sub(r'[-\|].*', '', string)

def generate_gpt_content(dict_data):
    article_list=list(dict())
    dict_data_updated = dict(list())
    added = 0
    # A simple check to see how many 'subsections' are present for the given key, so we dont write a shitty small 2 subheading article
    for key in dict_data.keys():
        if len(dict_data[key]) > 3:
            dict_data_updated[key] = dict_data[key]
            added+=1
    print("NEWLY ADDED FOR FURTHER WRITING = ", added)
    # Call the GPT API here
    for data in dict_data_updated.keys():
        print(f"STARTING FOR KEY {data}")
        dict_to_add={}
        dict_to_add['title']=paraphrase(data)
        print("-----------TITLE--------------")
        print(dict_to_add['title'])
        time.sleep(2)
        print("-----------SECTION--------------")

        for section in dict_data[data]:
            print("-----------SUBHEADING--------------")
            subheading=paraphrase(section['subheading'])
            print(subheading)
            time.sleep(2)
            text=paraphrase(section['text'])+"If you are"
            print("----------TEXT-----------")
            print(section['text'])
            print("TRANSFORMED TO \n")
            print(text)
            url_title=clean_up_title(section['URL Title'])
            print("-------URL TITLE---------")
            print(url_title)
            if 'AddionalTitle' in dict_to_add :
                dict_to_add['AdditionalTitle'].append(paraphrase(url_title))
            else:
                dict_to_add['AdditionalTitle']=[paraphrase(url_title)]
            # Use the original question+paraphrased text to align the intent
            gpt_text = text+"\n\n"+generate_long_form_content(section['subheading']+text)
            print("---------------GPT TEXT----------")
            print(gpt_text)
            subheading = generate_heading_for_content(gpt_text)
            print("NEW HEADING FOR SUBHEADING\n")
            print(subheading)
            # Generate long form content
            if 'sections' in dict_to_add:
                dict_to_add['sections'].append({"subheading":subheading, "content":gpt_text})
            else:
                dict_to_add['sections']=[{"subheading":subheading, "content":gpt_text}]
        intro_outro=enrich_with_intro_outro(dict_to_add)
        dict_to_add['intro'] = intro_outro['intro']
        dict_to_add['outro'] = intro_outro['outro']
        dict_to_add['description']=intro_outro['description']
        # dict_to_add['outro']=intro_outro['outro']
        article_list.append(dict_to_add)
        print("BREAKING HERE")
        break
    # new-dict here
    return article_list

def enrich_with_intro_outro(dict_to_add):
    text=dict_to_add['title']+"\n"
    text=text+convert_question_to_hook(text)+"\n"
    print("----CONVERTED TEXT TO HOOK----\n")
    print(dict_to_add['title']+":TO:"+text)
    suffix=""
    for value in dict_to_add['sections']:
        suffix=suffix+value['subheading']+"\n"
        suffix=suffix+value['content']+"\n"
    intro=text+get_text_with_suffix_prefix(text, suffix=suffix)
    print("---------GET TEXT WITH SUFFIX PREFIX------------")
    print(intro)
    intro += complete_sentences(intro+".In this article")
    print("AFTER COMPLETING THE SENTENCES")
    print(intro)
    description=complete_sentences("Write a blog description for article titled '"+dict_to_add['title']+"':")
    full_text = dict_to_add['title']+"\n"+intro+"\n"+suffix+"\nClosing thoughts:"
    outro=complete_sentences(full_text)
    print("FULLL TEXT - ", full_text)
    print("OUTRO", outro)
    # Generate description(SEO)
    # Generate intro
    # Generate outro
    return {"intro":intro, "description":description, "outro":outro}

def get_unique_keywords(title):
    # Get the stopwords
    stop_words = set(stopwords.words('english'))

    # Tokenize the sentence
    word_tokens = word_tokenize(title)

    # Filter the stopwords
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    # Filter the punctuations
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            if w != 'how':
                filtered_sentence.append(w)
    return " ".join(filtered_sentence)

def generate_image(title):
    sentence=get_unique_keywords(title)
    # Call the image generation pipeline
    return create_hero_image(hero_image_prompt_builder(sentence), height=512, width=512)

def strip_newline(string):
    return re.sub(r'\n|\t', '', string)


def write_to_file(dict_datas):
    # For title
    # Title/(Loop)Subheading/ Outro -> H2
    #       Text -> P
    
    for dict_data in dict_datas:
        now = datetime.datetime.now()
        now = now.strftime("%B %d, %Y %I:%M %p")
        print(f"Writing File at {now}")
        fileheader = "--- \n"\
                   f"title: {strip_newline(dict_data['title'])} \n"\
                    f"description: {strip_newline(dict_data['description'])} \n"\
                    f"category: general, air cooler \n"\
                    f"modified_date: {now} \n"\
                    f"date: {now} \n"\
                    f"image: /{generate_image(dict_data['title'])} \n"\
                    "---\n"
        fileheader += "<div>"
        html_data = ''
        html_data += '<p>' + dict_data['intro'] + '</p>\n'
        for section in dict_data['sections']:
            html_data += '<h3>' + section['subheading'] + '</h3>\n'
            html_data += '<p>' + section['content'] + '</p>\n'
        html_data += f'<h3>{random_conclusion()}</h3>\n'
        html_data += '<p>' + dict_data['outro'] + '</p>\n'
        fileclosing = "</div>"
        content_to_write=fileheader+html_data+fileclosing
        file_name = convert_string(dict_data['title'])
        with open(f"{POST_WRITE_PATH}/{file_name}.html", 'w') as file:
            file.write(content_to_write)

def convert_string(string):
    string = string.split()
    string = string[:5]
    string = '_'.join(string)
    string = string + '_' + hashlib.md5(string.encode()).hexdigest()
    return string 

def paa_engine_start():
    sanitized_dict_data = read_csv("home_cooler_6.csv")
    gpt_content=generate_gpt_content(sanitized_dict_data)
    write_to_file(gpt_content)
    # Metric Print (Time taken, word count, keyword density)
    # Publish

# return the new dictionary
def group_content(dict_to_add):
    new_dict = {}
    for article_no in len(dict_to_add):
        grouped_content = []
        for i in range(0, len(dict_to_add[article_no]['content']), 2):
            grouped_content.append({'question': dict_to_add[article_no]['content'][i]['question'], 'answer': dict_to_add[article_no]['content'][i+1]['answer']})
        new_dict[article_no] = {'grouped_content': grouped_content}
    return new_dict

# New pipeline
def generate_article_cluster_paa():
    print("STARTING.....")
    # Get the PAA
    sanitized_dict_data = read_csv("home_cooler_7.csv")
    # Generate Clusters and get the data back
    title_subheading = set()
    # for each key -> subheading, construct an array
    for title in sanitized_dict_data:
        for subheading in sanitized_dict_data[title]:
            title_subheading.add(subheading['subheading']+"\n"+subheading['text']+"\nurl:"+subheading['URL'])
    title_subheading=list(title_subheading)
    cluster_article = cluster_questions(title_subheading)
    article_to_generate=list(dict())
    for i, cluster in enumerate(cluster_article):
        if len(cluster) > 4:
            print(f"CLUSTER = {i}")
            print(f"cluster info = {cluster}")
            dict_to_add=dict()
            dict_to_add['article_no']=i
            content=list(dict())
            for sentence_id in cluster:
                question_answer = title_subheading[sentence_id].split("\nurl:")
                content.append({"question":question_answer[0], "answer":question_answer[1], "url":question_answer[1]})
            dict_to_add['content']=content
            article_to_generate.append(dict_to_add)
    with open('something.txt', 'w') as f:
        f.write(str(article_to_generate))
    # Pick 2 PAA (Possibly, from top to bottom - 2,3)
    # For each question, answer with the group
    # Generate content
    for article in article_to_generate:
        text_to_write=list()
        for content in article['content']:
            content_val=paraphrase_and_change_tone(read_and_summarize(content['url']))
            title=generate_title(content_val)
            content_to_para = split_text_to_para(content_val)
            content_to_add = ""
            for para in content_to_para:
                content_to_add += f"<p>{para}</p>"
            text_to_write.append(f"<h3>{title}</h3>\n{content_to_add}\n")
        now = datetime.datetime.now()
        now = now.strftime("%B %d, %Y %I:%M %p")
        text = "\n".join(text_to_write)
        title = generate_title(text[:500])
        description = clean_up_response(complete_sentences("Write a blog description for article titled '"+title+"':"))
        print(f"Writing File at {now}")
        fileheader = "--- \n"\
                    f"title: {title} \n"\
                    f"description: {description} \n"\
                    f"category: general, air cooler \n"\
                    f"modified_date: {now} \n"\
                    f"date: {now} \n"\
                    f"image: /{generate_image('home')} \n"\
                    "---\n"
        fileheader += "<div>"
        fileheader += "\n".join(text_to_write)
        fileclosing = "</div>"
        full_content = fileheader+fileclosing
        file_name = convert_string(title)
        with open(f"{POST_WRITE_PATH}/{file_name}.html", 'w') as file:
            file.write(full_content)
    # with open(SITEMAP_PATH, 'a') as file:
    #     file.writeline("")
    # Slap a subheading with czearing/czearing/article-title-generator
    # Generate the content - Outro, Intro maybe GPT3
    # Send for Writing

if __name__ == "__main__":
    print("START")
    generate_article_cluster_paa()
    # sanitized_dict_data = read_csv("home_cooler_7.csv")
    # # Generate Clusters and get the data back
    # title_subheading = set()
    # # for each key -> subheading, construct an array
    # for title in sanitized_dict_data:
    #     for subheading in sanitized_dict_data[title]:
    #         title_subheading.add(subheading['subheading']+"\n"+subheading['text'])
    # title_subheading=list(title_subheading)
    # clusters = cluster_questions(title_subheading)
    
    # for cluster in clusters:
    #     print("CLUSTER \n")
    #     for val in cluster:
    #         print(title_subheading[val]+"\n")
    # text="air cooler for home"
    # print(paraphrase(text))
# What to do?
# PAA Introduction - Take a PAA - 
# Answer, feed it and generate a intro (Idea1 - Question)
# Investigate if we can convert a question into a blog introduction
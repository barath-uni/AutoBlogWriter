# from pipeline.imagegen.stableDiffusionImageGenerator import id_generator
# from utils.format_text import format_the_para
import csv
from gptgenerator.gpt_content_writer import complete_sentences

import sys
import logging
import re
import json

logging.basicConfig(filename="log.txt",level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

def resize_arrays(array1, array2):
    # find the difference in length
    length_difference = abs(len(array1) - len(array2))

    # if the length of array1 is greater than array2, concatenate the last two elements of array1
    if len(array1) > len(array2):
        array1[-2:] = [''.join(array1[-2:])]

    # if the length of array2 is greater than array1, concatenate the last two elements of array2
    if len(array2) > len(array1):
        array2[-2:] = [''.join(array2[-2:])]

    # repeat the previous steps until the arrays have the same length
    while length_difference > 0:
        # if the length of array1 is greater than array2, concatenate the last two elements of array1
        if len(array1) > len(array2):
            array1[-2:] = [''.join(array1[-2:])]
        # if the length of array2 is greater than array1, concatenate the last two elements of array2
        if len(array2) > len(array1):
            array2[-2:] = [''.join(array2[-2:])]

        # update the length difference
        length_difference = abs(len(array1) - len(array2))

    return array1, array2

def split_title_paragraph(text, titles):
    # split the text into lines
    title_gap = False
    lines = text.split("\n")
    # Go through each line      
    index = list()
    titles_ind_iter = 0
    for title_it, line in enumerate(lines):
        title = titles[titles_ind_iter]
        # Match the index
        if title in line:
            index.append(title_it)
            try:
                title = titles[titles_ind_iter+1]
            except StopIteration as e:
                print("End")
        else:

            # Check if any other title after this titles_ind_iter is present
            titles_to_check = titles[titles_ind_iter+1:]
            for i, tit in enumerate(titles_to_check):
                if tit in line:
                    title_gap = True
                    index.append(title_it)
                    titles_ind_iter = titles_ind_iter+1+i
                    break


    # Check the length of index
    if len(index) < len(titles):
        all_title_present = False
        print("NOT ALL TITLES ARE PRESENT. Partially Built or the format has changed.")
    else:
        all_title_present = True
    title_paragraph = dict()
    print(index)
    # Loop through the indexes that match and get value between index[i] and index[i+1]
    for i in range(len(index)):
        index_val = index[i]
        if i+1 == len(index):
            title_paragraph[lines[index_val]] = lines[index_val+1:]
        else:
            title_paragraph[lines[index_val]] = lines[index_val+1:index[i+1]]
    return title_paragraph, all_title_present, title_gap

    # Store this to an array val[i]=text[index[i]:index[i+1]]

    # Handle edge case

    # exit

    # Check Line 0 = Title[0]

    # Set title_seen = true
    # Set the paragraph as empty list and continue

    # If paragraph is empty add the line to the paragraph

    # Check if the title i is present in it

    # If present, store the following lines in an array

    # If next title is present, reset the array




def initialize_with_topic_outline(MAIN_TOPIC, TOPIC_TITLE, WORD_COUNT, TOPIC_DESCRIPTION, PARAGRAPH_COUNT):
    START_SEQUENCE=f"""
I need an expert to explain {MAIN_TOPIC}.
What information do you need from me to generate a fun, in-depth explaining article?

To generate an example article, you will need to provide:

The topic of the article

The length of the article

Any desired keywords or topics to focus on

Ok, here you go:

Topic: “{TOPIC_TITLE}”
Length: {WORD_COUNT} words MINIMUM
Focus topic: ”{TOPIC_DESCRIPTION}”

First create a {PARAGRAPH_COUNT} paragraph article outline:

Paragraph 1: Introduction
"""
    intro_text = "Paragraph 1: Introduction\n\n"
    generate_text = complete_sentences(START_SEQUENCE)
    # Extract Paragraphs
    paragraph_titles = re.findall(r'Paragraph \d+: (.*)', intro_text+generate_text)
    paragraph_titles = [para_tit.strip() for para_tit in paragraph_titles]
    # print(generate_text)
    return START_SEQUENCE, intro_text+generate_text, paragraph_titles


def difference_list(array1, array2):
    for element in array1:
        # check if the element is present in array2
        if element in array2:
            # if it is, remove it from array1
            array1.remove(element)
    return array1

# def write_to_file(f_t, f_p):
#     title_to_write = f_t
#     para_to_write = f_p
#     if len(title_to_write) != len(para_to_write):
#         print(title_to_write)
#         print(para_to_write)
#         # Dump this to a file and then raise (Can be investigated later)
#         with open(f"failureDump{id_generator()}.txt", 'w') as f:
#             f.write(str(title_to_write)+str(para_to_write))
#         title_to_write, para_to_write = resize_arrays(title_to_write, para_to_write)
#     text = ""
#     for i in range(len(title_to_write)):
#         text += title_to_write[i] + "\n"
#         text += para_to_write[i] + "\n"
#     # Open the file and write to it
#     with open("SomethingBasic.html", 'w') as f:
#         f.write(text)

def get_paragraph(text, title):
    # Generate the paragraph for the given title
    paragraph = complete_sentences(text+title)
    return paragraph

def main(file_name, main_topic, title, desc):
    topic_title = file_name
    # Feed the first content and generate the subheadings
    start_sequence, start_text, titles = initialize_with_topic_outline(
        MAIN_TOPIC=main_topic, 
        TOPIC_TITLE=title, 
        WORD_COUNT=1100, 
        TOPIC_DESCRIPTION=desc, 
        PARAGRAPH_COUNT=7
    )
    text = start_sequence+start_text+"Write a detailed section for the following paragraph \n\n"
    title_paragraph_dict = {}
    # Util to parse the subheading and paragraph separately
    # Feed the text back in -> add Introduction\n -> Ask one of the PAA Question

    for title in titles:
        paragraph = get_paragraph(text, title)
        title_paragraph_dict[title] = paragraph
    
    with open(f'gpt_output/{topic_title}.json', 'w') as f:
        json.dump(title_paragraph_dict, f)


def read_and_create_gpt_content():
    import time
    list_of_dict=list(dict())
    with open('/home/barath/codespace/blogwriter/AutoBlogWriter/topic_title_maintopic.csv', 'r') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            list_of_dict.append({'file_name':row['TITLE'], 'main_topic':row['MAIN TOPIC'], 'title':row['TOPIC TITLE'], 'desc':row['TOPIC DESCRIPTION']})
    # Loop through the list and call main()
    for val in list_of_dict:
        main(val['file_name'], val['main_topic'], val['title'], val['desc'])
        time.sleep(60)
        logging.info('Sleeping So that YOU CAN INVESTIGATE!')
        print('Sleeping So that YOU CAN INVESTIGATE!')

def read_json_and_create_html():
    with open('')
    json_dict = 

if __name__ == "__main__":
    
    # Add it back to whatever is generated so far
    # Do a 1000 Token length response
    # If 7-9 paragraphs are present, exit. Else regenerate
    # See Response
    print('')

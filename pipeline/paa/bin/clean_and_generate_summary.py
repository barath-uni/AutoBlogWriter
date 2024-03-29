import csv
import re
from gptgenerator.datasummarizer import DataSummarizer
from pathlib import Path
import torch
import random
import pycountry
import json
from utils.process_site_and_summarize import read_and_get_wordcount


def random_conclusion(list=["In Summary", "Closing Thoughts", "Ultimately"]):
    return random.choice(list)


POST_WRITE_PATH=Path("/home/barath/codespace/coolerssstack/_posts")
SITEMAP_PATH=Path("/home/barath/codespace/coolerssstack/public/sitemap.xml")

url_list = list()
negative_words = ["pc", "computer", "ac", "ton"]

def deep_clean(row):
    for key in row:
        for country in pycountry.countries:
            if country.name in row[key]:
                return None
        # Negative words
        for word in negative_words:
            if word.lower() in key:
                return None

def sanitize(row):
    date_regex = re.compile(r'\d{1,2} \w+ \d{4}')
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
        # Generate Summary for this key and add it to the row
        # row['SUMMARY'] = DataSummarizer(text)
        # Read the url and see the word count, if it is more than 2000 then don't continue
        if row['URL'] in url_list:
            return None
        text, word_count = read_and_get_wordcount(row['URL'])
        if word_count == 0:
            return None
        if word_count > 2000:
            return None
        print(f"THE WORD COUNT FOR {row['URL']} ARTICLE IS", word_count)
        # Don't allow duplicate URL rows, this affects the datasummarizer
        url_list.append(row['URL'])
        row['SUMMARY'] = DataSummarizer(text) 
        return row


def read_csv(csv_to_read):
    csv_to_dict = dict()
    with open(csv_to_read, 'r') as file:
        csv_data = csv.DictReader(file)
        # Sanitize
        for row in csv_data:
            row = sanitize(row)
            if row:
                if row['Parent'] in csv_to_dict:
                    csv_to_dict[row['Parent']].append({'subheading': row['PAA Title'], 'text': row['Text'], 'URL': row['URL'], 'URL Title': row['URL Title'], 'SUMMARY':row['SUMMARY']})
                else:
                    csv_to_dict[row['Parent']] = [{'subheading': row['PAA Title'], 'text': row['Text'], 'URL': row['URL'], 'URL Title': row['URL Title'], 'SUMMARY':row['SUMMARY']}]
    return csv_to_dict


def clean_up_title(string):
    return re.sub(r'[-\|].*', '', string)


def store_dict(value):
    with open('dict_for_processing.json', 'w') as f:
        json.dump(value, f)


if __name__ == "__main__":
    import time
    start_time = time.time()
    csv_val = read_csv("../../home_cooler_8.csv")
    store_dict(csv_val)
    print("END TIME", time.time()-start_time)

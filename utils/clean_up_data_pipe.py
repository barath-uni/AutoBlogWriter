import csv
import re
import pycountry

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

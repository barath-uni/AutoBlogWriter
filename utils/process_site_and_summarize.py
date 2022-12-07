import requests
from bs4 import BeautifulSoup
import time
from gptgenerator.datasummarizer import DataSummarizer

def read_and_get_p_tags(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    print("URL:", url)
    # Send a request to the URL and retrieve the text
    try:
        response = requests.get(url, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, "html.parser")
        paragraphs = soup.find_all("p")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.get_text()
        return text
    except Exception as e:
        print("Exception ", e)
        return ""

def read_and_summarize(url):
    text = read_and_get_p_tags(url)
    print("BEFORE SUMMARIZING")
    print(text)
    summary = DataSummarizer(text)
    return summary

def text_and_wordcount(text):
    if text == "":
        return "", 0
    return text, len(text.split(" "))

def read_and_get_wordcount(url) -> int:
    return text_and_wordcount(read_and_get_p_tags(url))

if __name__ == "__main__":
    count = read_and_get_wordcount("https://www.dhani.com/services/one-freedom/finance-guides/best-air-cooler-in-india/")
    print(count)
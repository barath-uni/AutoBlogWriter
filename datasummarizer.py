# -*- coding: utf-8 -*-
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Object of automatic summarization.
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

def DataSummarizer(content):
    '''
    Entry point.

    Args:
        url:    target url.
    '''
    # Object of web scraping.
    # web_scrape = WebScraping()
    # Web-scraping.
    file = content.replace(":",".")
    tokens_input = tokenizer.encode("summarize: "+file, return_tensors='pt', max_length=512, truncation=True)
    ids = model.generate(tokens_input, min_length=120, max_length=600)
    summary = tokenizer.decode(ids[0], skip_special_tokens=True)
    return summary

if __name__ == "__main__":
    import sys

    # web site url.
    # url = sys.argv[1]
    file = "Coverage Area: This high-performance air cooler is suitable for rooms up to 12 square meters of the area under ideal conditions Clean Air with i-Pure Technology: With multistage filter it combats air pollution, odor-causing microorganisms, and allergies to give you fresh air. For effective cooling keep doors and windows open High-Efficiency Cooling: Long-lasting dura pump, high water retention capacity honeycomb pads and cool flow dispenser to distribute water evenly on all sides make your summer cool and refreshing Tank Capacity: When it comes to water capacity, this cooler has a 12-liter tank and a water level indicator to let you know when to refill it Powerful Blower: The high-speed blower provides cool air instantly, so now enjoy your summers comfortably Low Power Consumption: This energy-saving cooler for room uses only 170 watts (approximately) and can also be operated on inverters. So unwind this summer without worrying about bills and power cuts Easy-to-Use: Diet 12t is a sleek, compact, and powerful cooler that can be easily operated in low and tight spaces. Its ergonomic dial knobs provide easy operation and elegant looks"
    # Initialize the HuggingFace summarization pipeline
    # summarizer = pipeline("summarization")
    # summarized = summarizer(file, min_length=75, max_length=300)
    file = file.replace(":",".")
    print(f"BEFORE = {file}")
    # Print summarized text
    # print(summarized)
    # DataSummarizer(file)
    tokens_input = tokenizer.encode("summarize: "+file, return_tensors='pt', max_length=512, truncation=True)
    ids = model.generate(tokens_input, min_length=80, max_length=120)
    summary = tokenizer.decode(ids[0], skip_special_tokens=True)
    print(summary)
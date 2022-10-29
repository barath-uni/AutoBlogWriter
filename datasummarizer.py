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
    with open("summarizer.text", "r") as f:
        file = f.read()
    # Initialize the HuggingFace summarization pipeline
    # summarizer = pipeline("summarization")
    # summarized = summarizer(file, min_length=75, max_length=300)
    # file = file.replace(":",".")
    # print(f"BEFORE = {file}")
    # Print summarized text
    # print(summarized)
    # DataSummarizer(file)
    tokens_input = tokenizer.encode("summarize: "+file, return_tensors='pt', max_length=512, truncation=True)
    ids = model.generate(tokens_input, min_length=500, max_length=1000)
    summary = tokenizer.decode(ids[0], skip_special_tokens=True)
    print("FINAL\n")
    print(summary)
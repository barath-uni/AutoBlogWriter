from transformers import LEDTokenizer, LEDForConditionalGeneration
import torch
tokenizer = LEDTokenizer.from_pretrained("hyesunyun/update-summarization-bart-large-longformer")
model = LEDForConditionalGeneration.from_pretrained("hyesunyun/update-summarization-bart-large-longformer")

def DataSummarizer(content):
    '''
    Entry point.

    Args:
        url:    target url.
    '''
    # Object of web scraping.
    # web_scrape = WebScraping()
    # Web-scraping.
    # Preprocess paragraph
    input = "<EV> "+content
    inputs_dict = tokenizer(input, padding="max_length", max_length=2000, return_tensors="pt", truncation=True)
    input_ids = inputs_dict.input_ids
    attention_mask = inputs_dict.attention_mask
    global_attention_mask = torch.zeros_like(attention_mask)
    # put global attention on <s> token
    global_attention_mask[:, 0] = 1
    predicted_summary_ids = model.generate(input_ids, attention_mask=attention_mask, global_attention_mask=global_attention_mask)
    return tokenizer.batch_decode(predicted_summary_ids, skip_special_tokens=True)[0]


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
    DataSummarizer(file)
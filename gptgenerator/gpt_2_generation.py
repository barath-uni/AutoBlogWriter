from transformers import pipeline, set_seed
import re
import time

def generate_title(text):
    title_generator = pipeline('summarization', model='czearing/article-title-generator')
    title = title_generator(text, min_length=1, max_length=20, repetition_penalty=4.5)
    return title[0]['summary_text']

def generate_content(text):
    generator = pipeline('text-generation', model='gpt2')
    output=generator(text, max_length=400, num_return_sequences=1)
    return output[0]['generated_text']
import spacy
import language_check
import textstat
from textblob import TextBlob
import nltk

def check_for_grammar_and_style(text):
    blob = TextBlob(text)
    mistakes = blob.correct()
    return mistakes

def check_structure_of_text(text):
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    tagged = [nltk.pos_tag(sent) for sent in words]
    chunks = nltk.ne_chunk_sents(tagged)
    return chunks

def check_for_typos_and_grammar_errors(text):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text)
    return matches

def check_for_logical_consistency(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for sent in doc.sents:
        for word in sent:
            if word.dep_ == "contradiction":
                print("Possible contradiction found:", word)

def check_for_engaging_and_entertaining_content(text):
    readability_score = textstat.flesch_reading_ease(text)
    print(readability_score)


# Main program
keyword = input("Enter keyword: ")
title = input("Enter title: ")
word_count = int(input("Enter word count: "))

output = """

"""
mistakes = check_for_grammar_and_style(output)
chunks = check_structure_of_text(output)
matches = check_for_typos_and_grammar_errors(output)
check_for_logical_consistency(output)
check_for_engaging_and_entertaining_content(output)
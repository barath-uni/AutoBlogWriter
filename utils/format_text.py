from textblob import TextBlob
# So damn naive at this point

import random

def split_text_to_para(text):
    # Set the probabilities for each number.
    probabilities = [0.3, 0.3, 0.15, 0.15, 0.05, 0.05]

    # Generate a random number between 3 and 8.
    number = random.choices(range(3, 9), probabilities)[0]
    # Split the text into sentences and store them in a list.
    sentences = text.split(".")

    # Split the list of sentences into subgroups of the specified size.
    subgroups = []
    for i in range(0, len(sentences), number):
        subgroups.append(format_the_para(sentences[i:i+number]))
    return subgroups

def format_text(word, sentiment):
    f = word
    if sentiment > 0.5:
        # Choose a formatting option based on the sentiment level.
        if sentiment > 0.75:
            f = f.replace(word, "<i>{}</i>".format(word))
        elif sentiment > 0.5:
            f = f.replace(word, "<b>{}</b>".format(word))
        else:
            f = f.replace(word, "<u>{}</u>".format(word))
    elif sentiment > 0.4:
        f = f.replace(word, "\"{}\"".format(word))
    return f

def format_the_para(text):
    text = " ".join(text)
    blob = TextBlob(text)
    print(text)
    # Identify the most attractive words or phrases in the text.
    most_attractive = []
    for word in blob.words:
        print("WORD", word)
        print("SENTIMENT", TextBlob(word).sentiment)
        if TextBlob(word).sentiment.polarity > 0.4 or TextBlob(word).sentiment.subjectivity > 4:
            most_attractive.append(word)
    for phrase in blob.noun_phrases:
        if TextBlob(phrase).sentiment.polarity > 0.4 or TextBlob(phrase).sentiment.subjectivity > 0.4:
            most_attractive.append(phrase)
    print(most_attractive)
    # Format the most attractive words or phrases with a randomly chosen formatting option.
    formatted_text = list()
    for t in text.split(" "):
        f = t
        if f in most_attractive:
            formatted_text.append(format_text(f, TextBlob(f).sentiment.subjectivity+TextBlob(f).sentiment.polarity))
        else:
            formatted_text.append(format_text(f, TextBlob(f).sentiment.subjectivity+TextBlob(f).sentiment.polarity))
    print(formatted_text)
    return " ".join(formatted_text)

import nltk, string
from nltk.tokenize import sent_tokenize
from collections import OrderedDict
import numpy as np
from numpy import matrix
nltk.download('punkt')
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt') # if necessary...


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    # print(((tfidf * tfidf.T).A)[0,1])
    return ((tfidf * tfidf.T).A)[0,1]

def clear_similar_senteces():
    with open("keywordlist.txt", "r") as f:
        data = f.readlines()
    matrix_sim=[[cosine_sim(x,y) for x in data] for y in data]
    print(matrix_sim)
    matrix_sim=np.array(matrix_sim)
    out_sim = matrix_sim.mean(axis=0)
    outdata = list()
    for idx,val in enumerate(out_sim):
        if val < 0.3:
            outdata.append(data[idx])
    with open("keyclean.txt", "w") as fw:
        fw.writelines(outdata)

clear_similar_senteces()
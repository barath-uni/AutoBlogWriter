import collections
import requests
import xml.etree.ElementTree as ET
import re
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import random

proxy_list = '''
49.51.90.57:3128
157.90.174.98:3128
43.135.156.130:59394
89.38.98.236:80
198.59.191.234:8080
208.82.61.66:3128
170.39.116.114:3128
198.49.68.80:80
170.39.118.22:3128
192.99.34.64:1337
212.107.28.122:80
169.57.1.85:8123
197.242.159.51:80
165.154.236.248:80
138.201.35.213:1337
89.36.94.242:1337
177.22.187.153:80
139.99.237.62:80
185.191.76.84:80
209.182.239.62:80
154.26.134.214:80
83.229.72.174:80
20.111.54.16:80
117.251.103.186:8080
164.155.64.72:3128
209.146.105.244:80
49.207.36.81:80
64.225.97.57:8080
110.164.3.7:8888
43.206.81.172:80
134.238.252.143:8080
45.79.110.81:80
20.210.113.32:8123
20.24.43.214:8123
47.242.43.30:1080
93.114.194.26:1337
76.72.138.48:3128
104.148.36.10:80
209.146.104.51:80
15.235.150.136:80
80.48.119.28:8080
100.20.156.53:80
201.229.250.19:8080
43.153.216.218:1080
165.154.243.247:80
87.247.186.105:80
45.5.92.94:8137
37.32.22.223:80
41.188.149.78:80
92.84.56.10:50782
1.1.189.58:8080
110.39.165.10:8080
109.92.222.170:53281
187.130.139.197:8080
45.79.111.38:9994
85.159.214.61:1080
96.126.124.197:8113
198.11.175.192:8080
124.13.181.4:80
68.183.191.179:44290
221.132.18.26:8090
36.92.85.66:8080
149.129.187.190:3128
75.72.55.108:8118
133.242.171.216:3128
187.217.54.84:80
141.94.137.176:1337
83.229.73.175:80
8.209.64.208:8080
183.88.139.13:8080
36.93.5.25:9812
75.126.253.8:8080
58.27.59.249:80
209.146.19.62:55443
103.149.238.98:8080
165.22.252.212:40727
164.62.72.90:80
8.208.89.32:8080
82.165.21.59:80
185.213.167.97:80
43.255.113.232:8082
110.238.74.184:8080
181.215.178.58:1337
192.177.173.142:3128
45.15.163.171:5653
192.186.172.164:9164
45.130.127.186:8190
154.202.106.164:3128
107.152.170.153:9204
107.172.185.161:3128
192.177.165.61:3128
45.72.108.15:6069
185.230.47.148:6071
67.227.119.191:6520
107.152.223.121:9534
209.127.127.193:7291
38.15.155.209:3128
154.202.100.33:3128
38.15.154.63:3128
23.236.249.75:6125
198.12.112.246:5257
104.144.26.237:8767
45.127.250.77:5686
107.152.197.4:8026
198.23.214.168:6435
23.236.249.44:6094
84.21.189.188:5835
104.227.223.25:8112
104.224.90.138:6299
45.72.40.100:9194
138.128.69.170:8239
154.202.125.164:3128
144.168.253.12:3128
154.201.33.39:3128
192.177.129.139:3128
154.201.34.93:3128
138.128.97.31:7621
104.144.72.151:6183
45.72.40.51:9145
138.128.40.218:6221
104.168.25.20:5702
92.242.191.129:5617
45.151.253.74:6239
107.175.119.237:6765
154.202.106.156:3128
154.201.33.248:3128
50.16.45.86:3129
36.91.45.10:51672
201.150.117.8:999
67.227.119.2:6331
107.172.37.244:3128
38.15.153.130:3128
156.239.62.57:3128
192.177.139.127:3128
154.202.106.21:3128
192.177.158.115:3128
23.250.101.102:8154
38.15.153.200:3128
192.177.165.132:3128
45.13.234.151:5541
154.84.140.85:3128
45.127.250.181:5790
156.238.10.0:5082
192.177.140.248:3128
192.177.165.245:3128
192.177.160.72:3128
209.127.138.71:7168
138.128.121.178:9250
185.213.242.49:8513
45.199.132.192:3128
192.177.140.33:3128
154.202.103.192:3128
192.177.163.47:3128
107.172.38.187:3128
104.144.51.124:7655
198.46.241.183:6718
91.188.247.125:8085
104.168.126.207:3128
192.177.139.227:3128
156.239.62.48:3128
154.201.38.27:3128
192.177.166.242:3128
154.201.37.53:3128
192.177.163.102:3128
154.202.102.52:3128
192.177.163.69:3128
104.227.172.34:7612
154.83.40.248:3128
192.177.158.185:3128
45.130.60.1:9528
192.177.173.97:3128
192.177.93.129:3128
38.15.152.249:3128
104.168.66.55:3128
192.177.142.208:3128
154.202.103.96:3128
38.15.153.101:3128
45.130.60.88:9615
45.15.162.16:7577
192.177.129.130:3128
154.202.101.130:3128
154.202.106.74:3128
104.227.100.254:8335
192.186.172.192:9192
104.144.109.134:6219
144.168.253.184:3128
154.202.106.152:3128
192.177.129.76:3128
50.117.66.83:3128
192.177.140.25:3128
154.201.34.28:3128
38.15.152.144:3128
104.227.13.123:8682
171.22.116.114:6922
154.202.101.2:3128
192.3.48.98:6091
23.230.44.247:3128
192.177.93.66:3128
192.177.165.90:3128
154.201.37.183:3128
192.3.48.191:6184
154.201.34.158:3128
136.0.95.16:3128
192.177.165.191:3128
154.202.106.153:3128
192.177.142.246:3128
50.117.66.71:3128
45.224.229.63:9128
154.201.34.13:3128
154.202.105.7:3128
23.230.21.215:3128
192.177.139.28:3128
154.201.37.144:3128
154.202.106.108:3128
144.168.254.113:3128
154.202.103.120:3128
154.202.116.100:3128
216.172.136.110:3128
192.177.142.68:3128
192.177.142.149:3128
45.86.66.238:6491
154.202.106.111:3128
192.177.142.91:3128
136.0.95.157:3128
186.179.29.249:5563
192.177.170.108:3128
154.201.38.113:3128
154.202.100.216:3128
144.168.255.54:3128
154.202.102.115:3128
154.202.101.190:3128
38.15.154.162:3128
104.227.101.205:6266
192.177.139.137:3128
154.201.33.164:3128
209.127.96.14:7609
104.227.172.7:7585
216.172.136.199:3128
192.177.165.159:3128
192.177.163.77:3128
45.89.100.33:6084
107.172.37.30:3128
144.168.254.79:3128
154.84.140.51:3128
154.84.140.46:3128
144.168.254.182:3128
23.254.101.235:3128
138.128.38.247:6314
154.201.33.173:3128
154.84.140.12:3128
192.177.166.249:3128
192.177.129.150:3128
192.177.160.217:3128
107.172.185.227:3128
91.188.247.103:8085
107.172.37.76:3128
192.177.129.144:3128
154.202.105.66:3128
192.177.173.209:3128
154.202.106.136:3128
154.202.106.13:3128
154.201.33.87:3128
154.83.40.42:3128
45.151.253.90:6255
154.30.250.125:5166
192.177.170.116:3128
38.15.155.133:3128
104.227.120.12:7086
209.127.138.68:7165
38.15.152.85:3128
107.172.185.86:3128
92.118.53.233:6341
144.168.255.106:3128
38.15.152.116:3128
144.168.253.5:3128
45.12.129.223:5535
45.8.134.232:7248
192.177.158.214:3128
156.239.51.195:3128
154.202.100.163:3128
107.172.34.178:3128
209.127.143.249:8348
154.202.100.97:3128
192.177.93.105:3128
144.168.254.53:3128
154.202.112.8:3128
93.190.245.30:9056
45.199.132.34:3128
154.202.105.230:3128
144.168.254.232:3128
192.177.142.19:3128
23.254.101.149:3128
156.239.62.4:3128
192.177.160.32:3128
154.202.116.110:3128
157.52.174.62:6271
192.177.170.232:3128
192.177.160.27:3128
91.212.100.121:6697
104.168.126.21:3128
'''
proxies = proxy_list.split("\n")
proxies[:] = [item for item in proxies if item != '']
print("PROXIES")
print(proxies)
# input: list of sentences
# output: list of clusters of sentences
def cluster_sentences(sentences, nb_of_clusters=5):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
    kmeans = KMeans(n_clusters=nb_of_clusters)
    kmeans.fit(tfidf_matrix)
    clusters = collections.defaultdict(list)
    for i, label in enumerate(kmeans.labels_):
            clusters[label].append(sentences[i])
    return dict(clusters)

# input: list of sentences
# output: list of clusters of sentences
def cluster_sentences_with_stemming(sentences, nb_of_clusters=5):
    ps = PorterStemmer()
    sentences_stemmed = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        new_sentence = ""
        for token in tokens:
            new_sentence += ps.stem(token) + " "
        sentences_stemmed.append(new_sentence)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences_stemmed)
    kmeans = KMeans(n_clusters=nb_of_clusters)
    kmeans.fit(tfidf_matrix)
    clusters = collections.defaultdict(list)
    for i, label in enumerate(kmeans.labels_):
            clusters[label].append(sentences[i])
    return dict(clusters)

def flatten(l):
    return [item for sublist in l for item in sublist]

# get the sitemap.xml of a url
def get_sitemap(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    sitemap = requests.get(url, headers=headers)
    return sitemap.text

# get the links from the sitemap.xml
def get_links(sitemap):
    links = []
    root = ET.fromstring(sitemap)
    for child in root:
        for subchild in child:
            print(subchild.tag)
            if 'loc' in subchild.tag:
                links.append(subchild.text)
    return links
import time
# get the html document of a url
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # for i in range(1,11):
    #     proxy = random.choice(proxies)
    #     print("Request #%d"%i)
    #     try:
    response = requests.get(url, headers=headers)
        #     print(response)
        #     return response.text
        # except:
        #     print("Skipping. Connnection error")
        #     print("Retrying with a different proxy")
    print("SOMETHING")
    time.sleep(4)
    return response.text

# get the first paragraph from the html document
def get_first_paragraph(html):
    paragraph = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
    if paragraph:
        return [para for para in paragraph[1].split(".") if para != ''][:1]
    else:
        return None

def get_word_list(text):
    word_list = re.sub("[^\w]", " ",  text).split()
    return word_list

def get_top_10_words(word_list):
    word_freq = {}
    for word in word_list:
        if word not in word_freq:
            word_freq[word] = 0
        word_freq[word] += 1
    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_freq[:10]


url="https://voltcave.com/post-sitemap.xml"
sitemap = get_sitemap(url)
print(sitemap)
links = get_links(sitemap)
print(links)
first_paras = list()
for link in links:
    html = get_html(link)
    first_paras.append(get_first_paragraph(html))
all_sentences = flatten(first_paras)

with open("something.txt", 'r') as file2:
    all_sentences = file2.read()
all_sentences = all_sentences.split(".")
dict0 = cluster_sentences(all_sentences)
dict2 = cluster_sentences_with_stemming(all_sentences)
print(dict0)
# https://voltcave.com/make-keyboard-quieter/
# html = get_html("https://voltcave.com/make-keyboard-quieter/")
# first_para = get_first_paragraph(html)
# print(first_para)
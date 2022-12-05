import csv
import re
from nltk.stem import PorterStemmer
from keras.utils import pad_sequences
import seaborn as sns
from scipy.spatial.distance import pdist,squareform
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import transformers as transf
import torch
import matplotlib.pyplot as plt
import numpy as np
import pycountry
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer, util
from umap import UMAP
import spacy

nlp = spacy.load("en_core_web_md")

def read_csv(csv_to_read):
    csv_to_dict = dict()
    with open(csv_to_read, 'r') as file:
        csv_data = csv.DictReader(file)
        # Sanitize
        for row in csv_data:
            row = sanitize(row)
            if row:
                if row['Parent'] in csv_to_dict:
                    csv_to_dict[row['Parent']].append({'subheading': row['PAA Title'], 'text': row['Text'], 'URL': row['URL'], 'URL Title': row['URL Title']})
                else:
                    csv_to_dict[row['Parent']] = [{'subheading': row['PAA Title'], 'text': row['Text'], 'URL': row['URL'], 'URL Title': row['URL Title']}]
    return csv_to_dict


def sanitize(row):
    date_regex = re.compile(r'\d{1,2} \w+ \d{4}')
    
    for key in row:
        for country in pycountry.countries:
            if country.name in row[key]:
                return None
        mo = date_regex.search(row[key])
        if mo:
            return None
        if 'more items' in row[key].lower():
            return None
    return row

def generate_embeddings(paa_questions):
    # Topic clustering so we can have a look at the topics
    # Prepare embeddings
    # docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']
    # sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    # embeddings = sentence_model.encode(paa_questions, show_progress_bar=False)

    # # Train BERTopic
    # topic_model = BERTopic().fit(paa_questions, embeddings)
    # reduced_embeddings = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
    # # Run the visualization with the original embeddings
    # fig=topic_model.visualize_documents(paa_questions, embeddings=reduced_embeddings)
    # # fig = topic_model.visualize_hierarchy()
    # fig.write_html("file.html")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    corpus_embeddings = model.encode(paa_questions, batch_size=16, show_progress_bar=True, convert_to_tensor=True)
    # umap_embeddings_visualize(corpus_embeddings)
    clusters = util.community_detection(corpus_embeddings, min_community_size=4, threshold=0.7)
    # print(clusters)
    # # plt.figure(figsize=(60, 60))
    # # for i in range(len(clusters)):
    # #     plt.scatter(clusters[i, 0], clusters[i, 1])
    # #     plt.annotate('sentence ' + str(paa_questions[i]), (clusters[i, 0], clusters[i, 1]))
    # # plt.title('2D PCA projection of embedded sentences from BERT')
    # # plt.show()

    for i, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(i+1, len(cluster)))
        for sentence_id in cluster[0:3]:
            print("\t", paa_questions[sentence_id])
        print("\t", "...")
        for sentence_id in cluster[-3:]:
            print("\t", paa_questions[sentence_id])
    return clusters
    # Clustering with Kmeans is poor, that it is not able to capture the correct
    # # Perform kmean clustering
    # num_clusters = 15
    # clustering_model = KMeans(n_clusters=num_clusters)
    # clustering_model.fit(corpus_embeddings)
    # cluster_assignment = clustering_model.labels_

    # clustered_sentences = [[] for i in range(num_clusters)]
    # for sentence_id, cluster_id in enumerate(cluster_assignment):
    #     clustered_sentences[cluster_id].append(paa_questions[sentence_id])

    # for i, cluster in enumerate(clustered_sentences):
    #     print("Cluster ", i+1)
    #     print(cluster)
    #     print("")

def umap_embeddings_visualize(embeddings):
    umap_data = UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
    cluster = HDBSCAN(min_cluster_size=15,
                          metric='euclidean',                      
                          cluster_selection_method='eom').fit(embeddings)
    result = pd.DataFrame(umap_data, columns=['x', 'y'])
    result['labels'] = cluster.labels_
    print(result)
    # Visualize clusters
    fig, ax = plt.subplots(figsize=(20, 10))
    outliers = result.loc[result.labels == -1, :]
    clustered = result.loc[result.labels != -1, :]
    plt.scatter(outliers.x, outliers.y, color='#BDBDBD', s=0.05)
    plt.scatter(clustered.x, clustered.y, c=clustered.labels, s=0.05, cmap='hsv_r')
    plt.colorbar()
    plt.show()

def generate_cluster(paa_questions):
    tokenizer = transf.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = transf.DistilBertModel.from_pretrained('distilbert-base-uncased')
    input_tokens = []
    for i in paa_questions:
        input_tokens.append(tokenizer.encode(i, add_special_tokens=True))

    input_ids = pad_sequences(input_tokens, maxlen=100, dtype="long", value=0, truncating="post", padding="post")

    def create_attention_mask(input_id):
        attention_masks = []
        for sent in input_ids:
            att_mask = [int(token_id > 0) for token_id in sent]  # create a list of 0 and 1.
            attention_masks.append(att_mask)  # basically attention_masks is a list of list
        return attention_masks

    input_masks = create_attention_mask(input_ids)

    input_ids = torch.tensor(input_ids)
    attention_mask = torch.tensor(input_masks)

    # Get all the model's parameters as a list of tuples.
    params = list(model.named_parameters())

    print('The BERT model has {:} different named parameters.\n'.format(len(params)))

    print('==== Embedding Layer ====\n')

    for p in params[0:5]:
        print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))

    print('\n==== First Transformer ====\n')

    for p in params[5:21]:
        print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))

    print('\n==== Output Layer ====\n')

    for p in params[-4:]:
        print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    sentence_features = last_hidden_states[0][:, 0, :].detach().numpy()
    print(sentence_features)
    array_similarity = squareform(pdist(sentence_features, metric="euclidean"))
    # Way to fetch maybe 10-100 items that have a high cosine similarity and look at the 'description-relationship'
    svm=sns.heatmap(array_similarity)
    fig=svm.get_figure()
    fig.savefig(f"similaritycluster.png", dpi=400)
    pca = PCA(n_components=60)
    pca.fit(sentence_features)
    print(np.sum(pca.explained_variance_ratio_))
    pca_sentence_features = pca.transform(sentence_features)
    plt.figure(figsize=(60, 60))
    for i in range(len(pca_sentence_features)):
        plt.scatter(pca_sentence_features[i, 0], pca_sentence_features[i, 1])
        plt.annotate('sentence ' + str(paa_questions[i]), (pca_sentence_features[i, 0], pca_sentence_features[i, 1]))
    plt.title('2D PCA projection of embedded sentences from BERT')
    plt.show()

def generate_clusterr():
    # Model for computing sentence embeddings. We use one trained for similar questions detection
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # We donwload the Quora Duplicate Questions Dataset (https://www.quora.com/q/quoradata/First-Quora-Dataset-Release-Question-Pairs)
    # and find similar question in it
    url = "http://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"
    dataset_path = "quora_duplicate_questions.tsv"
    max_corpus_size = 50000  # We limit our corpus to only the first 50k questions


    # Check if the dataset exists. If not, download and extract
    # Download dataset if needed
    if not os.path.exists(dataset_path):
        print("Download dataset")
        util.http_get(url, dataset_path)

    # Get all unique sentences from the file
    corpus_sentences = set()
    with open(dataset_path, encoding='utf8') as fIn:
        reader = csv.DictReader(fIn, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            corpus_sentences.add(row['question1'])
            corpus_sentences.add(row['question2'])
            if len(corpus_sentences) >= max_corpus_size:
                break

    corpus_sentences = list(corpus_sentences)
    print("Encode the corpus. This might take a while")
    corpus_embeddings = model.encode(corpus_sentences, batch_size=64, show_progress_bar=True, convert_to_tensor=True)


    print("Start clustering")
    start_time = time.time()

    #Two parameters to tune:
    #min_cluster_size: Only consider cluster that have at least 25 elements
    #threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
    clusters = util.community_detection(corpus_embeddings, min_community_size=25, threshold=0.75)

    print("Clustering done after {:.2f} sec".format(time.time() - start_time))

    #Print for all clusters the top 3 and bottom 3 elements
    for i, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(i+1, len(cluster)))
        for sentence_id in cluster[0:3]:
            print("\t", corpus_sentences[sentence_id])
        print("\t", "...")
        for sentence_id in cluster[-3:]:
            print("\t", corpus_sentences[sentence_id])


import numpy as np

def cluster_questions(questions_answers):
    # Create a list of documents, where each document is a question and answer
    documents = []
    for question_answ in questions_answers:
        document = nlp(question_answ)
        documents.append(document)

    similarity_matrix = np.zeros(shape=(len(questions_answers), len(questions_answers)))
    for i,doc1 in enumerate(documents):
        for j,doc2 in enumerate(documents):
            # Create a similarity matrix to compare the similarity between each document
            similarity_matrix[i][j] = doc1.similarity(doc2)
    # Use k-means clustering to group the documents into clusters
    kmeans = KMeans(n_clusters=len(questions_answers) // 3)
    clusters = kmeans.fit_predict(similarity_matrix)

    # Group the questions and answers into their respective clusters
    clustered_questions = []
    for cluster_id in range(kmeans.n_clusters):
        cluster_questions = []
        for i, cluster in enumerate(clusters):
            if cluster == cluster_id:
                cluster_questions.append(i)
        clustered_questions.append(cluster_questions)

    return clustered_questions



# # Read csv
# csv_to_dict = read_csv("home_cooler_6.csv")
# title_subheading = set()
# # for each key -> subheading, construct an array
# for title in csv_to_dict:
#     for subheading in csv_to_dict[title]:
#         title_subheading.add(subheading['subheading']+subheading['text'])
# title_subheading=list(title_subheading)
# new_title_sh = list()
# print("NUMBER OF QUESTIONS", len(title_subheading))
# generate_embeddings(title_subheading)
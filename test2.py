import re

# list of words
words = ['commonsense reasoning [32]', 'question answering [63]', 'recommendation systems [57]', 'entities [22]', 'RotatE [45]', 'ComplEx [15]', 'ConvE [16]', 'TransE [4]', 'transformers [49]', 'BERT [17]', 'KGBert [62]', 'Bert for Link Prediction (BLP) [14]', 'StAR [51]', 'Commonsense [32]', 'SimKGC [53]', 'BERTRL [64]', 'Graph Neural Networks (GNN) [39] [27]', 'MaKEr [?]', 'RMPI [20]', 'TransH [?]', 'RESCAL [?]', 'R-GCN [41]', 'CompGCN [49]', 'NeuralLP [60]', 'DRUM [37]', 'LAN [54]', 'GraIL [46]', 'StaTIK[33]']

# regular expression pattern to match the references
pattern = r'^(\w+\s*)+\[(\d+)+\]'

# iterate over the words and extract the matching references
matching_references = []
for word in words:
    match = re.search(pattern, word)
    if match:
        print(match.group(2))
        matching_references.append(match.group(0))

# display the matching references
for reference in matching_references:
    print(reference)

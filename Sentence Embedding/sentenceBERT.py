from sentence_transformers import SentenceTransformer
import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize
import numpy as np

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

# other trained models at
# https://github.com/UKPLab/sentence-transformers/blob/master/docs/pretrained-models/sts-models.md

sentences = ["I'm pissed of",
             "I'm really happy",
             "I'm upset"]

sentence_embeddings = sbert_model.encode(sentences)
query = "I'm really angry"
query_vec = sbert_model.encode([query])[0]


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

for sent in sentences:
  sim = cosine(query_vec, sbert_model.encode([sent])[0])
  print("Sentence = ", sent, "; similarity = ", sim)

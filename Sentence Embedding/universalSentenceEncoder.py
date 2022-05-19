import tensorflow as tf
import tensorflow_hub as hub
from nltk.tokenize import word_tokenize
import numpy as np
import nltk
nltk.download('punkt')

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print("module %s loaded" % module_url)


sentences = ["I'm pissed of",
             "I'm really happy",
             "I'm upset"]

sentence_embeddings = model(sentences)
query = "I'm really angry"
query_vec = model([query])[0]

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

for sent in sentences:
  sim = cosine(query_vec, model([sent])[0])
  print("Sentence = ", sent, "; similarity = ", sim)
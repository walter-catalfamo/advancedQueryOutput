import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize
import numpy as np

from gensim.models.doc2vec import Doc2Vec, TaggedDocument


sentences = ["I ate dinner.",
       "We had a three-course meal.",
       "I had pizza and pasta",
       "Brad came to dinner with us.",
       "He loves fish tacos.",
       "In the end, we all felt like we ate too much.",
       "We all agreed; it was a magnificent evening."]

tokenized_sent = []
for s in sentences:
    tokenized_sent.append(word_tokenize(s.lower()))
tokenized_sent

# si potrebbero eliminare gli elementi di punteggiatura da tokenized_sent

tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]
tagged_data

model = Doc2Vec(tagged_data, vector_size = 20, window = 2, min_count = 1, epochs = 100)

test_doc = word_tokenize("I had pizza and pasta".lower())
test_doc_vector = model.infer_vector(test_doc)
similarity_array = model.docvecs.most_similar(positive = [test_doc_vector])
similarity_array

# def cosine(u, v):
#     return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
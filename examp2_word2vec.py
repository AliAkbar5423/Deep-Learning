import codecs
import glob
import multiprocessing
import os
import pprint
import re
import nltk
import gensim.models.word2vec as w2v
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from nltk import word_tokenize 

file_buku = sorted(glob.glob("corpus/melekpolitik.txt"))
#"Kalau mau pakai semua korpus"#
##file_buku = sorted(glob.glob("corpus/*.txt"))
print("file ditemukan: ")
file_buku

corpus_raw = u""
for file_books in file_buku:
    print("Reading '{0}'...".format(file_books))
    with codecs.open(file_books, "r", encoding="utf8") as book_file:
        corpus_raw += book_file.read()
    print("Corpus is now {0} characters long".format(len(corpus_raw)))
    print()

raw_sentences = word_tokenize(corpus_raw)

#convert into a list of words
#rtemove unnnecessary,, split into words, no hyphens
#list of words
def sentence_to_wordlist(raw):
    clean = re.sub("[^a-zA-Z]"," ", raw)
    words = clean.split()
    return words

sentences = []
for raw_sentence in raw_sentences:
    if len(raw_sentence) > 0:
        sentences.append(sentence_to_wordlist(raw_sentence))

print(raw_sentences[5])
print(sentence_to_wordlist(raw_sentences[5]))

token_count = sum([len(sentence) for sentence in sentences])
print("The book corpus contains {0:,} tokens".format(token_count))

#ONCE we have vectors
#step 3 - build model
#3 main tasks that vectors help with
#DISTANCE, SIMILARITY, RANKING

# Dimensionality of the resulting word vectors.
#more dimensions, more computationally expensive to train
#but also more accurate
#more dimensions = more generalized
num_features = 300
# Minimum word count threshold.
min_word_count = 3

# Number of threads to run in parallel.
#more workers, faster we train
num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 7

# Downsample setting for frequent words.
#0 - 1e-5 is good for this
downsampling = 1e-3

# Seed for the RNG, to make the results reproducible.
#random number generator
#deterministic, good for debugging
seed = 1

hate2vec = w2v.Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=num_features,
    min_count=min_word_count,
    window=context_size,
    sample=downsampling
)

hate2vec.build_vocab(sentences)
print("Panjang Kosakata word2vec:", len(hate2vec.wv.vocab))

print (hate2vec.most_similar('Protes'))

vocab = list(hate2vec.wv.vocab)
X = hate2vec[vocab]
#X = hate2vec[hate2vec.wv.vocab]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'], df['y'])
for word, pos in df.iterrows():
    ax.annotate(word, pos)

plt.show()
#plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
#plt.title('Hasil')
#plt.show()
hate2vec.train(sentences, total_examples=hate2vec.corpus_count, epochs=hate2vec.iter)
if not os.path.exists("trained"):
    os.makedirs("trained")

hate2vec.save(os.path.join("trained", "hate2vec.w2v"))



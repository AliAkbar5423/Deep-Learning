# load text
filename = 'sketsa.txt'
file = open(filename, 'rt', encoding='latin-1')
text = file.read()
file.close()

# split into words by white space
words = text.split()

# split based on words only
import re
words = re.split(r'\W+', text)

# remove punctuation from each word
import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in words]

# convert to lower case
words = [word.lower() for word in words]

# split into sentences
from nltk import sent_tokenize
sentences = sent_tokenize(text)

# split into words
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)

# remove remaining tokens that are not alphabetic
words = [word for word in stripped if word.isalpha()]

# filter out stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('indonesian'))
words = [w for w in words if not w in stop_words]

file_baru = 'sketsac.csv'
pb = open(file_baru, 'w')
pb.write(str(words))
print(words)

pb.write(str(words))
print(words)
pb.close()

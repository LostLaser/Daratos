import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
import pandas
import pickle
import csv

docs1 = ['Well done!',
		'Good work',
		'Great effort',
		'nice work',
		'Excellent!']

colnames = ['publication','content']
#data= pandas.read_csv('all-the-news/articles2.csv', nrows=1000, names = colnames, error_bad_lines=False)
#docs = data.content.tolist()
#print (docs)
bias_list_train = []
content_list_train = []
bias_list_test = []
content_list_test = []
docs=[]
line_count = 0
with open('all-the-news/articles2.csv', encoding='utf8', errors='replace') as csv_file:
		csv_reader = csv.reader(csv_file)
		for row in csv_reader:
			docs.extend([row[1]])
print(len(docs))
# create the tokenizer
t = Tokenizer(num_words=15000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
# fit the tokenizer on the documents
t.fit_on_texts(docs)
#print(t.word_docs)

encoded_docs = t.texts_to_sequences(docs1)
print(encoded_docs)

with open('tokenizer.pickle', 'wb') as handle:
	pickle.dump(t, handle, protocol=pickle.HIGHEST_PROTOCOL)

exit()
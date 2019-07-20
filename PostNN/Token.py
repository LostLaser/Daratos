import numpy
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
import pandas
import pickle
import csv

docs1 = ['Well done is a great phrase!',
		'Good work everyone! Now it is time for the second',
		'Great effort',
		'nice workers',
		'Excellent! excellent']

colnames = ['publication','content']
bias_list_train = []
content_list_train = []
bias_list_test = []
content_list_test = []
docs=[]
line_count = 0

with open('all-the-news/articles2_cleaned.csv', encoding='utf8', errors='replace') as csv_file:
		csv_reader = csv.reader(csv_file)
		for row in csv_reader:
			if(line_count != 0):
				row_content = row[1]
				docs.extend([row_content])
				if(line_count > 20000):
					break
			line_count+=1

print(len(docs))
#print(docs[1])
# create the tokenizer
t = Tokenizer(num_words=15000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
# fit the tokenizer on the documents
t.fit_on_texts(docs)
#print(t.word_index)

encoded_docs = t.texts_to_sequences(docs)
#print(encoded_docs)
print(len(docs[0]))
print(encoded_docs[0])
print("Word count: "+str(t.num_words))

with open('tokenizer.pickle', 'wb') as handle:
	pickle.dump(t, handle, protocol=pickle.HIGHEST_PROTOCOL)

exit()
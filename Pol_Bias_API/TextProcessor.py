import nltk
import pickle
import string
import re
import numpy
from keras.preprocessing import sequence as sqc

class ProcessRaw:
    max_words = 50

    def __init__(self):
        with open('../Pol_Bias_ML/SentenceNN/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        self.stemmer = nltk.stem.PorterStemmer()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def full_clean(self, content):
        if not content:
            return [[]]
        content=content.lower()
        content=re.sub(r'\d+', '', content)
        content=content.translate(str.maketrans('','', string.punctuation))
        content=content.strip()
        print(content)
        tokens=nltk.tokenize.word_tokenize(content)
        content=" ".join([self.stemmer.stem(i) for i in tokens if not self.stemmer.stem(i) in self.stop_words])
        encoded_content = self.tokenizer.texts_to_sequences([content])
        encoded_content = sqc.pad_sequences(encoded_content, maxlen=self.max_words)
        content_train = numpy.array(encoded_content)
        print(content_train)
        return content_train
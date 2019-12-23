import pickle
import string
import re
import numpy
from keras.preprocessing import sequence as sqc
import nltk

nltk.download("stopwords")
nltk.download("punkt")

class ProcessRaw:
    max_words = 50
    stemmer = None
    tokenizer = None
    stop_words = None

    def __init__(self):
        with open('./tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
            
        self.stemmer = nltk.stem.PorterStemmer()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        
    def split_sentences(self, content):
        '''
        Splits the content into sentences.

        Parameters: 
            content (str): String of words
    
        Returns: 
            list: Sentences created from the input string
        '''
        sentence_list = []
        for sentence in re.split(r'\!|\.|\?',content):
            sentence= re.sub(r'@[a-zA-Z0-9|_]+', '', sentence)
            if not sentence == '':
                sentence_list.append(sentence)
        
        return sentence_list

    def full_clean_sentence(self, content):
        '''
        Greatly simplifies the input string into its' root meaning.
        Does not handle punctuation.

        Parameters: 
            content (str): String of words
    
        Returns: 
            str: Fully cleaned string
        '''
        if not content:
            return [[]]
        content = content.lower()
        content = re.sub(r'\d+', '', content)
        content = content.translate(str.maketrans('','', string.punctuation))
        content = content.strip()
        tokens = nltk.tokenize.word_tokenize(content)
        content = " ".join([self.stemmer.stem(i) for i in tokens if not self.stemmer.stem(i) in self.stop_words])
        encoded_content = self.tokenizer.texts_to_sequences([content])
        encoded_content = sqc.pad_sequences(encoded_content, maxlen=self.max_words)
        content_train = numpy.array(encoded_content)

        return content_train

    def full_clean_article(self, content):
        '''
        Greatly simplifies the input string into its' root meaning.
        Able to handle punctuation in the input string.

        Parameters: 
            content (str): String of words
    
        Returns: 
            list[list]: tokenized sentences
            list[str]: Sentences split on sentence boundaries
        '''
        content_sentences = self.split_sentences(content)
        tokenized_sentences = list(map(self.full_clean_sentence, content_sentences))

        return tokenized_sentences, content_sentences

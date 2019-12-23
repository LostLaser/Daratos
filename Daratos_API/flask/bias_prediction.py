import numpy
import keras
import tensorflow as tf
import os
from keras.models import load_model
import text_processor

class Predictor():
    def __init__(self):
        try:
            self.full_processor = text_processor.ProcessRaw()
        except OSError:
            print("INFO: Missing tokenizer file. Prediction will not be made.")
            self.full_processor = None
        try:
            self.model = load_model('./sentenceModel.h5')
            self.model._make_predict_function()
        except IOError:
            print("INFO: Running in skeleton mode. Predictions will not be made.")
            self.model = None
        self.graph = tf.get_default_graph()

    def predict_article(self, content):
        '''
        Performs predictions on the sentences inside of input string.

        Parameters: 
            content (str): A portion of text

        Returns: 
            list: The prediction values for each of the sentences
            list: A list of sentences created from the input string
        '''
        if self.model is None or self.full_processor is None:
            raise EnvironmentError
        
        #Tokenizing the sentences that are inside of input content
        tokenized_sentences, content_sentences = self.full_processor.full_clean_article(content)
        
        #Making predictions on each of the sentences
        predictions = []
        
        with self.graph.as_default():
            for sentence in tokenized_sentences:
                predictions.extend(self.model.predict_classes(sentence).tolist())

        return predictions, content_sentences

    def consolidate_biases(self, bias_list):
        '''
        Calculates an overall bias score for the specified sentence biases.

        Parameters: 
            bias_list (list): A list of sentence bias predictions (numbers 0-2)

        Returns: 
            string: A label representing the determined bias
        '''
        left_count, right_count = 0, 0

        for prediction in bias_list:
            if prediction == 0:
                left_count += 1
            if prediction == 2:
                right_count += 1

        left_percentage = left_count/len(bias_list)
        right_percentage = right_count/len(bias_list)
        determination = "neutral"
        if left_percentage > right_percentage and left_percentage > 0.1:
                determination = "left"
        elif right_percentage > 0.1:
                determination = "right"

        return determination

    def tokenize_sentences(self, content):
        tokenized_sentences, _ = self.full_processor.full_clean_article(content)

        return tokenized_sentences
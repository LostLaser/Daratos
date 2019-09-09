from keras.models import load_model
import text_processor
import numpy
import keras
import tensorflow as tf

#Loading items needed for prediction
try:
    full_processor = text_processor.ProcessRaw()
except OSError:
    full_processor = None
try:
    model = load_model('sentenceModel.h5')
    model._make_predict_function()
except IOError:
    model = None
graph = tf.get_default_graph()


def predict_article(content):
    '''
        Performs predictions on the sentences inside of input string.

        Parameters: 
            content (str): A portion of text
    
        Returns: 
            list: The prediction values for each of the sentences
            list: A list of sentences created from the input string
        '''
    if model is None or full_processor is None:
        raise EnvironmentError
    
    #Tokenizing the sentences that are inside of input content
    content_sentences = full_processor.split_sentences(content)
    tokenized_sentences = list(map(full_processor.full_clean, content_sentences))

    #Making predictions on each of the sentences
    predictions = []
    with graph.as_default():
        for sentence in tokenized_sentences:
            predictions.extend(model.predict_classes(sentence).tolist())

    return predictions, content_sentences

def determine_article_bias(bias_list):
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
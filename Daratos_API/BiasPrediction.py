from keras.models import load_model
import TextProcessor
import numpy
import keras
import tensorflow as tf

#Loading items needed for prediction
try:
    full_processor = TextProcessor.ProcessRaw()
except OSError:
    full_processor = None
try:
    model = load_model('sentenceModel.h5')
    model._make_predict_function()
except IOError:
    model = None
graph = tf.get_default_graph()


def predict_article(content):
     
    if model is None or full_processor is None:
        raise EnvironmentError
    
    #Tokenizing the sentences that are inside of input content
    content_sentences = full_processor.split_sentences(content)
    tokenized_sentences = list(map(full_processor.full_clean, content_sentences))

    #Making predictions on each of the sentences
    predictions = []
    with graph.as_default():
        for sentence in tokenized_sentences:
            predictions.extend(model.predict(sentence).tolist())

    return predictions, content_sentences
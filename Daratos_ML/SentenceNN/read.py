import csv
import numpy
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
import pickle

data_list = ['../Labeling/out_file.csv']

def load_data():
    train_split=0.75
    left_list_content = []
    left_list_bias = []
    neutral_list_content = []
    neutral_list_bias = []
    right_list_content = []
    right_list_bias = []
    
    for source in data_list: 
        with open(source, encoding='utf8', errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            red_count = 0
            for row in csv_reader:
                if line_count !=0:
                    #Sentence is labeled as left
                    if row[2] == 'l':
                        left_list_bias.append(0)
                        left_list_content.append(row[1])
                    #Sentence is labeled as neutral
                    elif row[2] == 'n':
                        neutral_list_bias.append(1)
                        neutral_list_content.append(row[1])
                    #Sentence is labeled as right
                    elif row[2] == 'r':
                        right_list_bias.append(2)
                        right_list_content.append(row[1])
                        red_count += 1
                    
                    
                line_count += 1

    print("Left leaning sentences: " + str(len(left_list_bias)))
    print("Neutral sentences: " + str(len(neutral_list_bias)))
    print("Right leaning sentences: " + str(len(right_list_bias)))
    print("Training-testing split: "+str(train_split))

    # Split the data into training and testing categories
    bias_list_train, bias_list_test = train_test_split([left_list_bias, neutral_list_bias, right_list_bias], train_split)
    content_list_train, content_list_test = train_test_split([left_list_content, neutral_list_content, right_list_content], train_split)

    # create the tokenizer from file
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # Tokenize input contents for neural network
    encoded_content_train = tokenizer.texts_to_sequences(content_list_train)
    encoded_content_test = tokenizer.texts_to_sequences(content_list_test)
    bias_list_train = to_categorical(bias_list_train)
    bias_list_test = to_categorical(bias_list_test)

    content_train = numpy.array(encoded_content_train)
    bias_train = numpy.array(bias_list_train)
    content_test = numpy.array(encoded_content_test)
    bias_test = numpy.array(bias_list_test)
    
    return (content_train, bias_train),(content_test,bias_test), tokenizer.num_words 

def train_test_split(bias_lists, split_percent):
    '''
    Splits the content into sentences.

    Parameters: 
        content (str): String of words
        split_percent(decimal): percentage of the data to leave in the training category

    Returns: 
        list: Sentences created from the input string
    '''
    if split_percent > 1:
        return [], []
    
    list_train = []
    list_test = []
    for bias_list in bias_lists:
        list_train.extend(bias_list[:int(len(bias_list)*split_percent)])
        list_test.extend(bias_list[int(len(bias_list)*split_percent):])

    return list_train, list_test

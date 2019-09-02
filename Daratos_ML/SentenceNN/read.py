import csv
import numpy
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
import pickle

data_list = ['../Labeling/out_file.csv']

def load_data():
    train_split=0.75
    left_list_cont = []
    left_list_bias = []
    neutral_list_cont = []
    neutral_list_bias = []
    right_list_cont = []
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
                        left_list_cont.append(row[1])
                    #Sentence is labeled as neutral
                    elif row[2] == 'n':
                        neutral_list_bias.append(1)
                        neutral_list_cont.append(row[1])
                    #Sentence is labeled as right
                    elif row[2] == 'r':
                        right_list_bias.append(2)
                        right_list_cont.append(row[1])
                        red_count += 1
                    
                    
                line_count += 1

    #neutral_list_bias = neutral_list_bias[:200]
    #neutral_list_cont = neutral_list_cont[:200]
    print("Left leaning sentences: " + str(len(left_list_bias)))
    print("Neutral sentences: " + str(len(neutral_list_bias)))
    print("Right leaning sentences: " + str(len(right_list_bias)))
    print("Training-testing split: "+str(train_split))

    bias_list_train = right_list_bias[:int(len(right_list_bias)*train_split)]
    bias_list_train.extend(left_list_bias[:int(len(left_list_bias)*train_split)])
    bias_list_train.extend(neutral_list_bias[:int(len(neutral_list_bias)*train_split)])

    content_list_train = right_list_cont[:int(len(right_list_cont)*train_split)]
    content_list_train.extend(left_list_cont[:int(len(left_list_cont)*train_split)])
    content_list_train.extend(neutral_list_cont[:int(len(neutral_list_cont)*train_split)])

    bias_list_test = right_list_bias[int(len(right_list_bias)*train_split):]
    bias_list_test.extend(left_list_bias[int(len(left_list_bias)*train_split):])
    bias_list_test.extend(neutral_list_bias[int(len(neutral_list_bias)*train_split):])

    content_list_test = right_list_cont[int(len(right_list_cont)*train_split):]
    content_list_test.extend(left_list_cont[int(len(left_list_cont)*train_split):])
    content_list_test.extend(neutral_list_cont[int(len(neutral_list_cont)*train_split):])

    # create the tokenizer from file
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    
    encoded_content_train = tokenizer.texts_to_sequences(content_list_train)
    encoded_content_test = tokenizer.texts_to_sequences(content_list_test)
    bias_list_train = to_categorical(bias_list_train)
    bias_list_test = to_categorical(bias_list_test)

    content_train = numpy.array(encoded_content_train)
    bias_train = numpy.array(bias_list_train)
    content_test = numpy.array(encoded_content_test)
    bias_test = numpy.array(bias_list_test)
    
    return (content_train, bias_train),(content_test,bias_test), tokenizer.num_words 

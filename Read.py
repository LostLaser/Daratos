import csv
import numpy
from keras.preprocessing.text import Tokenizer
import pickle

left_leaning = ['Atlantic', 'Buzzfeed News', 'Guardian', 'New York Times', 'CNN', 'Vox', 'Washington Post']
#right_leaning = ['Breitbart', 'National Review','New York Post']
right_leaning = ['Fox News', 'National Review', 'New York Post', 'Breitbart']

def load_data():
    bias_list_train = []
    content_list_train = []
    bias_list_test = []
    content_list_test = []
    
    with open('all-the-news/articles2.csv', encoding='utf8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        red_count = 0
        for row in csv_reader:
            #reading only content rows
            if line_count !=0:
                #checking if source is right leaning
                for source in right_leaning:
                    if source == row[0]:
                        bias_list_train.append(1)
                        content_list_train.append(row[1])
                        red_count += 1
                #checking if source is left leaning
                for source in left_leaning:
                    if source == row[0]:
                        bias_list_train.append(0)
                        content_list_train.append(row[1])
            line_count += 1

    with open('all-the-news/articles3.csv', encoding='utf8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        red_count = 0
        for row in csv_reader:
            #reading only content rows
            if line_count !=0:
                #checking if source is right leaning
                for source in right_leaning:
                    if source == row[0]:
                        bias_list_train.append(1)
                        content_list_train.append(row[1])
                        red_count += 1
                #checking if source is left leaning
                for source in left_leaning:
                    if source == row[0]:
                        bias_list_train.append(0)
                        content_list_train.append(row[1])
            line_count += 1

    with open('all-the-news/articles1.csv', encoding='utf8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        red_count = 0
        for row in csv_reader:
            #reading only content rows
            if line_count !=0:
                #checking if source is right leaning
                for source in right_leaning:
                    if source == row[0]:
                        bias_list_test.append(1)
                        content_list_test.append(row[1])
                        red_count += 1
                #checking if source is left leaning
                for source in left_leaning:
                    if source == row[0]:
                        bias_list_test.append(0)
                        content_list_test.append(row[1])
            line_count += 1

    # create the tokenizer from file
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    #t = Tokenizer(num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')

    
    encoded_content_train = tokenizer.texts_to_sequences(content_list_train)
    encoded_content_test = tokenizer.texts_to_sequences(content_list_test)
    #print(type(encoded_content_train))

    content_train = numpy.array(encoded_content_train)
    bias_train = numpy.array(bias_list_train)
    content_test = numpy.array(encoded_content_test)
    bias_test = numpy.array(bias_list_test)
    
    #print(content_train)

    #print(arr)
    #print(type(content_train))
    #print(type(bias_train))
    #print(red_count)
    #print(len(content_train))
    #print(len(bias_train))
    #print(len(content_test))
    #print(len(bias_test))

    return (content_train, bias_train),(content_test,bias_test), len(tokenizer.word_index) + 1 

#load_data()
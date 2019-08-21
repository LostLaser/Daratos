import nltk
import string
import re
import csv
import clean_string


def clean(file_name):
    docs=[]
    line_count=0
    stop_words = set(nltk.corpus.stopwords.words('english'))
    stemmer = nltk.stem.PorterStemmer()
    with open(file_name, encoding='utf8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if(line_count != 0):
                row_content = clean_string.clean(row[1], stemmer, stop_words)
                docs.append([row[0],row_content])
            else:
                docs.append([row[0],row[1]])
            line_count+=1
    print("Writing to new file...")
    with open('cleaned_file.csv', mode='w', encoding='utf8', newline='') as cleaned_file:
        news_writer = csv.writer(cleaned_file, delimiter=',')
        for entry in docs:
            news_writer.writerow([entry[0], entry[1]])
        
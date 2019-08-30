import nltk
import string
import re
import csv

def clean(file_name):
    '''
    Divides the csv entries from the sources specified into sentences.

    Parameters: 
        file_name (str): File to read from in csv format
  
    Returns: 
        csv file
    '''
    docs=[]
    line_count=0
    stop_words = set(nltk.corpus.stopwords.words('english'))
    stemmer = nltk.stem.PorterStemmer()
    with open(file_name, encoding='utf8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if(line_count != 0):
                row_content = clean_string(row[1], stemmer, stop_words)
                docs.append([row[0],row_content])
            else:
                docs.append([row[0],row[1]])
            line_count+=1
    print("Writing to new file...")
    with open('cleaned_file.csv', mode='w', encoding='utf8', newline='') as cleaned_file:
        news_writer = csv.writer(cleaned_file, delimiter=',')
        for entry in docs:
            news_writer.writerow([entry[0], entry[1]])

def clean_string(input_string, stemmer, stop_words):
    '''
    Greatly simplifies the input string into its' root meaning.

    Parameters: 
        input_string (str): File to read from in csv format
  
    Returns: 
        str: Fully cleaned string
    '''
    row_content = input_string
    row_content=row_content.lower()
    row_content=re.sub(r'\d+', '', row_content)
    row_content=row_content.translate(str.maketrans('','', string.punctuation))
    row_content=row_content.strip()
    tokens=nltk.tokenize.word_tokenize(row_content)
    row_content=" ".join([stemmer.stem(i) for i in tokens if not stemmer.stem(i) in stop_words])
    return row_content
        
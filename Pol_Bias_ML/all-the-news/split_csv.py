import string
import re
import csv


def convert(file_name):
    source_list=['Vox']
    docs=[]
    line_count=0
    with open(file_name, encoding='utf8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if(row[0] in source_list):
                row_content = row[1]
                for sentence in re.split(r'\!|\.|\?',row_content):
                    sentence= re.sub(r'@[a-zA-Z0-9|_]+', '', sentence)
                    if re.match(r"[a-zA-Z0-9|_|:|;|,|,|\"|ï¿½]+",sentence):
                        docs.append([row[0], sentence, line_count])
            elif(line_count == 0):
                docs.append([row[0],row[1], "Source_Line"])
            line_count+=1
    print("Writing to new file...")
    with open('split_file.csv', mode='w', encoding='utf8', newline='') as split_file:
        news_writer = csv.writer(split_file, delimiter=',')
        for entry in docs:
            if(entry[1].strip() != '' and len(entry[1].strip()) > 75):
                news_writer.writerow([entry[0], entry[1], entry[2]])
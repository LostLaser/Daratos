import nltk
import string
import re


def clean(inp, stemmer, stop_words):
	row_content = inp
	row_content=row_content.lower()
	row_content=re.sub(r'\d+', '', row_content)
	row_content=row_content.translate(str.maketrans('','', string.punctuation))
	row_content=row_content.strip()
	tokens=nltk.tokenize.word_tokenize(row_content)
	row_content=" ".join([stemmer.stem(i) for i in tokens if not stemmer.stem(i) in stop_words])
	return row_content

def test_clean():
	docs1 = ['   Well     done is a great phrase!',
		'Good work everyone! Now it is time for the second',
		'Great effort',
		'  nice         workers',
		'Excellent! excellent   ']
	stops = set(nltk.corpus.stopwords.words('english'))
	stems = nltk.stem.PorterStemmer()
	for row in docs1:
		row_content = clean(row, stems, stops)
		print(row_content)
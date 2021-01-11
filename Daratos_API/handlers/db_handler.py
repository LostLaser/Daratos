import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import config
from dto import db_entities


try:
    # Set up connection to firestore
    cred = credentials.Certificate(config.DB_CONFIG_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except:
    db = None
    print("WARN: Using local website scrapping information\n")
    local_db = {
        'www.cnn.com': '//*[@id="body-text"]/div[1]',
        'www.foxnews.com': '//*[@id="wrapper"]/div[2]/div[1]/main/article/div/div/div[1]/p',
        'www.nytimes.com': '//*[@id="story"]/section/div/div/p'
    }
    

# retrieve xpath from database
def get_xpath(domain):
    x_path = ""

    if db:
        doc_ref = db.collection(u'NewsSite').document(domain)
        news_doc = doc_ref.get()
        if news_doc.exists:
            x_path = news_doc.to_dict().get('xpath')
    else:
        x_path = local_db.get(domain)

    return x_path

def is_bias_stored(url, content):
    if not db:
        return False
    
    doc_ref = db.collection(u'StoredBiases').document(content)
    doc = doc_ref.get()

    return doc.exists

def get_stored_bias(url, content):
    if not db:
        print("Unable to connect to the database")
        return

    doc_ref = db.collection(u'StoredBiases').document(content)

def store_bias(url, content, bias_value):
    if not db:
        return
    predicted_entry = db_entities.PredictedEntry(content, url, bias_value)
    db.child(u'StoredBiases').push(predicted_entry)
    
# check if database connection is healthy
def db_health():
    try:
        db.collection(u'NewsSite')
        return "UP"
    except:
        return "DOWN"


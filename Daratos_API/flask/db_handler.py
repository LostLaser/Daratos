import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

try:
    # Set up connection to firestore
    cred = credentials.Certificate('./api_config.json')
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
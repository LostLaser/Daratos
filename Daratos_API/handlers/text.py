from newspaper import fulltext
from handlers import api_exception

def extract(raw_html):
    text = ""
    try:
        text = fulltext(raw_html)
    except Exception as e:
        raise api_exception.InvalidUsage('Unable to extract text. Are you sure this is html?', status_code = 422)

    if len(text) <= 0:
        raise api_exception.InvalidUsage('No content found', status_code = 204)

    return text

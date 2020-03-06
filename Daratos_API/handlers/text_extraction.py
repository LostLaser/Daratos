from newspaper import fulltext


def extract(raw_html):
    text = ""
    try:
        text = fulltext(raw_html)
    except:
        return None

    if len(text) <= 0:
        return None

    return text



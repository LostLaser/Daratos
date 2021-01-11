class PredictedEntry:
    content_hash = ""
    web_address = ""
    bias_value = 0.0

    def __init__(self, content_hash, web_address, bias_value):
        self.content_hash = content_hash
        self.web_address = web_address
        self.bias_value = bias_value   
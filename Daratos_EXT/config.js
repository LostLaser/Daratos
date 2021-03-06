var config = {
    "daratos_api_url": "http://127.0.0.1:8080",
    "ERR_GENERIC": "Oh no! Something went wrong.",
    "ERR_NO_CONTENT": "No content found!",
    "ERR_RETRY": "There was a problem, please try again.",
    "ERR_BIAS_CONNECTION": "Oh no! Unable to connect to bias predictor.",
    "MAX_BIAS": 42.0,
    "MIN_BIAS": -42.0
};

// production variables
chrome.management.getSelf(function(result){
    var env = result.installType
    if (env != "development") {
        config["daratos_api_url"] = "https://www.daratos.app"
    }
})

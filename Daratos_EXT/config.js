var config = {
    "daratos_api_url": "http://127.0.0.1:8080"
};

// production variables
chrome.management.getSelf(function(result){
    var env = result.installType
    if (env != "development") {
        config["daratos_api_url"] = "https://"
    }
})

function setPopupMessage(output_message) {
    document.getElementById("output_box").innerHTML = output_message;
    document.getElementById("loader").hidden = true;
}

document.addEventListener("DOMContentLoaded", function(){
    
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
            let word = response.content_dirty
            console.log(word);

            let url = "http://127.0.0.1:5000/bias?content="+String(word);
            function getBias() {
                if (word.length > 0) {
                    fetch(url)
                        .then(
                            function(response) {
                                if (response.status !== 200) {
                                    setPopupMessage("Whoops! Looks like there was a problem.")
                                    console.log('Looks like there was a problem. Status Code: ' +
                                    response.status);
                                    return;
                                }
                                response.json().then(function(data) {
                                    setPopupMessage(data.total_bias);
                                });
                        })
                        .catch(setPopupMessage("Oh no! Unable to connect to bias predictor."));
                }
                else {
                    setPopupMessage("No content found!")
                }
            }

            getBias();
        });
    });
    
});


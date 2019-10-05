document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("bias_button").onclick = fetch_bias;   
});

function fetch_bias(){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
            let word = response.content_dirty

            setLoading();
            let url = "http://127.0.0.1:5000/bias?content="+String(word);
            function getBias() {
                if (word.length > 0) {
                    fetch(url)
                        .then(
                            function(response) {
                                if (response.status !== 200) {
                                    setPopupMessage("Whoops! Looks like there was a problem.")
                                    console.log('There was a problem. Status Code: ' + response.status);
                                    return;
                                }
                                response.json().then(function(data) {
                                    setPopupMessage(data.total_bias);
                                });
                        })
                        .catch(function(response) {
                            if (!response.ok) {
                                setPopupMessage("Oh no! Unable to connect to bias predictor.");
                            }
                            return response;
                        })
                }
                else {
                    setPopupMessage("No content found!")
                }
            }

            getBias();
        });
    });
    
}

function setPopupMessage(output_message) {
    document.getElementById("output_box").innerHTML = output_message;
    document.getElementById("loader").hidden = true;
}

function setLoading() {
    document.getElementById("bias_button").hidden = true;
    document.getElementById("loader").hidden = false;
}
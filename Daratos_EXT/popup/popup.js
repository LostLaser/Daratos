var config = chrome.extension.getBackgroundPage().config;

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("bias_button").onclick = fetch_bias;  
});

function fetch_bias(){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {}, function(response) {
            setLoading()
            let web_content = response.text_content;
            
            if (web_content) {
                bias_call_options = {
                    method: 'post',
                    body: JSON.stringify({raw_html: String(web_content)}),
                    headers: {'Content-Type': 'application/json'}
                }   
                call_api(config.daratos_api_url + "/bias/html", bias_call_options).then(function(response){    
                    if (response.total_bias) {
                        setPopupMessage(response.total_bias);
                    }
                    else {
                        setPopupMessage("Oh no! Something went wrong.")
                    }
                });
            }
            else {
                setPopupMessage("No content found!");
            }
        });

    });
}

// safely call api with specified options
async function call_api(url, options) {
    setLoading();
    
    var return_val;

    let response = await fetch(url, options)
        .catch(function(response) {
            console.log(response)
            return response;
        });

    if (! response.status) {
        setPopupMessage("Oh no! Unable to connect to bias predictor.");
    }
    else if (response.status !== 200) {
        setPopupMessage("Whoops! Looks like there was a problem.");
        console.log('There was a problem. Status Code: ' + response.status);
    }
    else {
        return_val = await response.json()
    }
    
    return return_val;
}

function setPopupMessage(output_message) {
    document.getElementById("bias_button").classList.add("hide")
    document.getElementById("output_box").innerHTML = output_message;
    document.getElementById("loader").classList.add("hide")
}

function setLoading() {
    document.getElementById("bias_button").classList.add("hide")
    document.getElementById("output_box").innerHTML = "";
    document.getElementById("loader").classList.remove("hide")
}
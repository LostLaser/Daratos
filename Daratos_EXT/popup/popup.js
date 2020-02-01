var config = chrome.extension.getBackgroundPage().config;

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("bias_button").onclick = fetch_bias;  
});

function fetch_bias(){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let pathArray = tabs[0].url.split('/');
        let domain = pathArray[2];
        let domain_xpath = "";
        call_options = {
            method: 'post',
            body: JSON.stringify({domain: String(domain)}),
            headers: {'Content-Type': 'application/json'}
        }
        call_api(config.daratos_api_url + "/article/xpath", call_options).then(function(response){    
            if (! response) {
                return
            }

            domain_xpath = response.domain_xpath

            if (! domain_xpath) {
                setPopupMessage("This website is not supported yet.");
                return
            }
            
            chrome.tabs.sendMessage(tabs[0].id, {xpath: domain_xpath}, function(response) {
                let web_content = response.text_content;
                
                if (web_content) {
                    bias_call_options = {
                        method: 'post',
                        body: JSON.stringify({content: String(web_content)}),
                        headers: {'Content-Type': 'application/json'}
                    }   
                    call_api(config.daratos_api_url + "/bias", bias_call_options).then(function(response){    
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
    console.log(return_val)
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
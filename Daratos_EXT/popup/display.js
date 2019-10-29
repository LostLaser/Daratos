document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("bias_button").onclick = fetch_bias;   
});

function fetch_bias(){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let pathArray = tabs[0].url.split('/')
        let host = pathArray[2]
        if (host == 'www.foxnews.com') {
            domain_xpath = '//div/p'
        }
        chrome.tabs.sendMessage(tabs[0].id, {xpath: domain_xpath}, function(response) {
            let content = response.text_content

            setLoading();
            
            if (content.length > 0) {
                call_api("http://127.0.0.1:5000/bias?content="+String(content)).then(function(response){    
                    if (response.length > 0) {
                        setPopupMessage(response)
                    } 
                });
            }
            else {
                setPopupMessage("No content found!")
            }

        });
    });
    
}

async function call_api(url) {
    let return_val = "";

    let response = await fetch(url)
        .catch(function(response) {
            return response;
        });

    if (response.status == undefined) {
        setPopupMessage("Oh no! Unable to connect to bias predictor.");
    }
    else if (response.status !== 200) {
        setPopupMessage("Whoops! Looks like there was a problem.");
        console.log('There was a problem. Status Code: ' + response.status);
    }
    else {
        let data = await response.json()
        return_val = data.total_bias;
    }

    return return_val;
}

function setPopupMessage(output_message) {
    document.getElementById("bias_button").hidden = true;
    document.getElementById("output_box").innerHTML = output_message;
    document.getElementById("loader").hidden = true;
}

function setLoading() {
    document.getElementById("bias_button").hidden = true;
    document.getElementById("output_box").innerHTML = "";
    document.getElementById("loader").hidden = false;
}
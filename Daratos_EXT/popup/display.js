document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("bias_button").onclick = fetch_bias;   
});

function fetch_bias(){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let pathArray = tabs[0].url.split('/');
        let host = pathArray[2];
        let host_xpath = "//div/p";
        // call_api("http://127.0.0.1:5000/article/xpath", {
        //         method: 'post',
        //         body: JSON.stringify({host: String(host)}),
        //         headers: {
        //             'Content-Type': 'application/json'
        //         }
        //     }).then(function(response){    
        //         host_xpath = response.host_xpath
        //     });
        if (! host_xpath) {
            setPopupMessage("This website is not supported yet.");
            return
        }
        
        chrome.tabs.sendMessage(tabs[0].id, {xpath: host_xpath}, function(response) {
            let web_content = response.text_content;

            setLoading();
            
            if (web_content) {
                call_api("http://127.0.0.1:5000/bias", {
                    method: 'post',
                    body: JSON.stringify({content: String(web_content)}),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(function(response){    
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
    document.getElementById("bias_button").hidden = true;
    document.getElementById("output_box").innerHTML = output_message;
    document.getElementById("loader").hidden = true;
}

function setLoading() {
    document.getElementById("bias_button").hidden = true;
    document.getElementById("output_box").innerHTML = "";
    document.getElementById("loader").hidden = false;
}
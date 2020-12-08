var config = chrome.extension.getBackgroundPage().config;

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("bias_button").onclick = fetch_bias
    showBiasButton()
});

function fetch_bias(){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {}, function(response) {

            setLoading();
            let web_content = "";
            
            if (typeof response == "undefined") {
                setPopupMessage(config.ERR_RETRY)
                return
            }

            web_content = response.text_content
            
            if (web_content) {
                bias_call_options = {
                    method: 'post',
                    body: JSON.stringify({raw_html: String(web_content)}),
                    headers: {'Content-Type': 'application/json'}
                }   
                call_api(config.daratos_api_url + "/bias/html", bias_call_options)
            }
            else {
                setPopupMessage(config.ERR_NO_CONTENT);
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
            return response;
        });

    console.log(response.status)
    if (! response.status) {
        setPopupMessage(config.ERR_BIAS_CONNECTION);
    }
    else if (response.status == 204) {
        setPopupMessage(config.ERR_NO_CONTENT);
    } else if (response.status == 504) {
        setPopupMessage(config.ERR_BIAS_CONNECTION)
        console.log('There was a problem. Status Code: ' + response.status);
    }
    else if (response.status < 200 || response.status >= 300) {
        setPopupMessage(config.ERR_GENERIC);
        console.log('There was a problem. Status Code: ' + response.status);
    }
    
    json_response = await response.json()
    if (json_response.total_bias) {
        // setPopupMessage(json_response.total_bias);
        setBiasResult(12);
    }
}

function setPopupMessage(output_message) {
    hideAll()
    document.getElementById("output_box").classList.remove("hide")
    document.getElementById("output_box").innerHTML = output_message
}

function setBiasResult(bias_num) {
    hideAll()
    var scale = document.getElementById("bias_output")
    scale.classList.remove("hide")
    scale.value = 12
}

function setLoading() {
    hideAll()
    document.getElementById("loader").classList.remove("hide")
}

function showBiasButton() {
    hideAll()
    document.getElementById("bias_button").classList.remove("hide")
}

function hideAll() {
    document.getElementById("bias_button").classList.add("hide")
    document.getElementById("loader").classList.add("hide")
    document.getElementById("output_box").classList.add("hide")
    document.getElementById("bias_output").classList.add("hide")
}

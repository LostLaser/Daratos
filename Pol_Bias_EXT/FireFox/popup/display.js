//createCanvas()
document.addEventListener("DOMContentLoaded", function(){
    console.log("setup");
    
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
            let word = response.content_dirty
            console.log(word);

            let url = "http://127.0.0.1:5000/bias?content="+String(word);
            async function getUserAsync() 
            {
                let response = await fetch(url);
                let data = await response.json()
                return data;
            }

            getUserAsync()
                .then(data => document.getElementById("output_box").innerHTML = data.lean);
        });
    });
    
});
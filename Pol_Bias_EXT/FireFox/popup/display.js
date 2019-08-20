//createCanvas()
document.addEventListener("DOMContentLoaded", function(){
    console.log("setup");
    let back_page = chrome.extension.getBackgroundPage();
    let word = back_page.word.trim();
    console.log(word)
    
    let url = "http://127.0.0.1:5000/bias";

    async function getUserAsync(name) 
    {
        let response = await fetch(url);
        let data = await response.json()
        return data;
    }

    getUserAsync('yourUsernameHere')
        .then(data => document.getElementById("output_box").innerHTML = data.lean);
});
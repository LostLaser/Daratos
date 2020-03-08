chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {

        let markup = document.documentElement.innerHTML;
        
        let message = {
            text_content: markup
        };
        console.log(markup)
        sendResponse(message)
    });
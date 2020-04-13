chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let markup = document.getElementsByTagName("body")[0].innerHTML;
        
        let message = {
            text_content: markup
        };
        
        sendResponse(message)
    });
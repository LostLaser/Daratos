chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let selectedText = window.getSelection().toString()
        let message = {
            content_dirty: selectedText
        };
        sendResponse(message);
    });
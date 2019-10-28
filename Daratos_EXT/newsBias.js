chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let selectedText = ""

        let query = document.evaluate('//div/p', document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        for (let i = 0, length = query.snapshotLength; i < length; ++i) {
            let elementText = query.snapshotItem(i).textContent
            console.log(elementText);
            selectedText += String(elementText)
        }

        let message = {
            content_dirty: selectedText
        };
        sendResponse(message)
    });
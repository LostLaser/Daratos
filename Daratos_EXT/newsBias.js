chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let selectedText = ""
        let xpath = request.xpath
        console.log(xpath)

        let query = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        for (let i = 0, length = query.snapshotLength; i < length; ++i) {
            let elementText = query.snapshotItem(i).textContent
            console.log(elementText);
            selectedText += String(elementText)
        }

        let message = {
            text_content: selectedText
        };
        sendResponse(message)
    });
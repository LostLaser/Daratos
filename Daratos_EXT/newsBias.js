chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let selectedText = ""
        let xpath = request.xpath

        let query = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        for (let i = 0, length = query.snapshotLength; i < length; ++i) {
            let elementText = query.snapshotItem(i).textContent
            selectedText += String(elementText)
        }
        let markup = document.documentElement.innerHTML;
        console.log(markup)
        let message = {
            text_content: selectedText
        };
        sendResponse(message)
    });
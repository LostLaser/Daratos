window.addEventListener('mouseup', itemSelected);

function itemSelected() {
    let selectedText = window.getSelection().toString()
    if (selectedText.length > 0) {
        let message = {
            text: selectedText
        };
        chrome.runtime.sendMessage(message);
    }
}
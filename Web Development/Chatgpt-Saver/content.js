//content.js
function getReplies() {
  const elements = document.querySelectorAll('[data-message-author-role="assistant"]');
  const replies = [];
  elements.forEach(el => {
    const text = el.innerText.trim();
    console.log("🧩 Found reply text:", text); // debug stays
    if (text && !replies.includes(text)) replies.push(text);
  });
  return replies;
}

function saveReplies() {
    const replies = getReplies();
    console.log("🧩 Found replies:", replies); // debug stays

    chrome.storage.local.get("saverEnabled", ({ saverEnabled }) => {
        if (!saverEnabled) {
            console.log("Replies saver disabled, skipping save."); // debug stays
            return;
        }

        try {
            chrome.runtime.sendMessage({ type: "SAVE_REPLIES", data: replies }, (response) => {
                if (chrome.runtime.lastError) {
                    console.warn("Message not sent:", chrome.runtime.lastError.message);
                } else {
                    console.log("Replies sent successfully:", response);
                }
            });
        } catch (e) {
            console.warn("Extension context invalidated:", e);
        }
    });
}

let saveTimeout;
const observer = new MutationObserver(() => {
  clearTimeout(saveTimeout);
  saveTimeout = setTimeout(saveReplies, 1000);
});
observer.observe(document.body, { childList: true, subtree: true });

// Stop observing on unload (fixes “Extension context invalidated”)
window.addEventListener("unload", () => {
  observer.disconnect();
  console.log("🧹 Disconnected observer on unload.");
});

// Initial run
saveReplies();
console.log("✅ Content script loaded and observing for replies.");

chrome.runtime.onMessage.addListener((msg) => {
  console.log("📩 got message:", msg);
});

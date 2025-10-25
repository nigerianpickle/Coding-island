//popup.js

let enabled = false;
const btn = document.getElementById('toggleBtn');

btn.addEventListener('click', () => {
    enabled = !enabled;
    btn.textContent = enabled ? "Disable" : "Enable";

    // Save the state to chrome.storage so content script can read it
    chrome.storage.local.set({ saverEnabled: enabled });
});

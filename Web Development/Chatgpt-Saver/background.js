//background.js
chrome.runtime.onMessage.addListener(async (msg) => {
  if (msg.type === "SAVE_REPLIES") {
    const { data } = msg;
    const { replies = [] } = await chrome.storage.local.get("replies");
    const combined = [...replies, ...data];
    await chrome.storage.local.set({ replies: combined });
    console.log("💾 Saved", data.length, "new replies. Total:", combined.length);
  }
});

chrome.runtime.onStartup.addListener(printReplies);
chrome.runtime.onInstalled.addListener(printReplies);

async function printReplies() {
  const { replies = [] } = await chrome.storage.local.get("replies");
  console.log("🧠 All saved replies:");
  replies.forEach((r, i) => console.log(`#${i + 1}:`, r));
}

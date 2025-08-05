
async function send() {
const input = document.getElementById("input");
const chat = document.getElementById("chat");

const userMessage = input.value.trim();
if (!userMessage) return;

console.log("📤 Sending:", userMessage);
// Add user message to chat
chat.innerHTML += `<div class="message user">${userMessage}</div>`;
chat.scrollTop = chat.scrollHeight;

// Send to backend
const response = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage })
});

const data = await response.json();
const botReply = data.reply;

// Add bot reply to chat
chat.innerHTML += `<div class="message bot">${botReply}</div>`;
chat.scrollTop = chat.scrollHeight;

// Clear input
input.value = "";
input.focus();
}
window.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("input");
input.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      send();
    }
    });
  }); 
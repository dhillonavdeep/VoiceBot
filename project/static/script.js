document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    const userInput = document.getElementById("userInput");
    const chatLog = document.getElementById("chatLog");

    async function fetchAnswer(question) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", "bot-message");
        messageDiv.textContent = "Thinking...";
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;

        const res = await fetch("/answer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        const data = await res.json();
        messageDiv.textContent = data.answer;
        chatLog.scrollTop = chatLog.scrollHeight;
        speakText(data.answer);
    }

    sendBtn.addEventListener("click", () => {
        const question = userInput.value.trim();
        if (question) {
            const userMessageDiv = document.createElement("div");
            userMessageDiv.classList.add("message", "user-message");
            userMessageDiv.textContent = question;
            chatLog.appendChild(userMessageDiv);
            userInput.value = "";
            fetchAnswer(question);
        }
    });

    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendBtn.click();
        }
    });

    async function speakText(text) {
        if (!text) return;
        console.log("Speaking:", text);  // Debugging print
        const res = await fetch("/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        if (res.ok) {
            console.log("Text spoken successfully.");
        } else {
            console.error("Failed to speak text.");
        }
    }
});
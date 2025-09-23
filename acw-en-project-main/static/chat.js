const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatBody = document.getElementById('chat-body');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;
    addMessage('user', message);
    chatInput.value = '';
    chatInput.disabled = true;
    addMessage('bot', '...');
    const botMsgDiv = chatBody.querySelector('.bot:last-child');
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        botMsgDiv.textContent = data.response;
    } catch (err) {
        botMsgDiv.textContent = 'Sorry, there was an error.';
    } finally {
        chatInput.disabled = false;
        chatInput.focus();
        chatBody.scrollTop = chatBody.scrollHeight;
    }
});

function addMessage(sender, text) {
    const div = document.createElement('div');
    div.className = sender;
    div.textContent = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
} 
const chatContainer = document.getElementById('chatContainer');
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');

questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !sendButton.disabled) {
        sendQuestion();
    }
});

function addMessage(text, isUser, isWin = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    
    if (isWin) {
        const winBadge = document.createElement('span');
        winBadge.className = 'win-indicator';
        winBadge.textContent = 'WIN!';
        bubble.appendChild(winBadge);
    }
    
    messageDiv.appendChild(bubble);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendQuestion() {
    const question = questionInput.value.trim();
    if (!question) return;

    addMessage(question, true);
    questionInput.value = '';
    sendButton.disabled = true;

    const gameId = document.getElementById('gameId').value;
    const body = JSON.stringify({'text' : question, 'game_id' : gameId})
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        });
        const data = await response.json();
        const win = data.win;
        if (win) {
            addMessage("You win!!", false);
        } else {
            addMessage(data.answer, false);
        }
    } catch (error) {
        addMessage('Error: Could not get response', false);
        console.error('Error:', error);
    } finally {
        sendButton.disabled = false;
        questionInput.focus();
    }
}

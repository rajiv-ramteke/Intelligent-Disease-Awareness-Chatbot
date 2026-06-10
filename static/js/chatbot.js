const Chatbot = {
    sessionId: null,
    chatWindow: null,
    inputField: null,
    sendBtn: null,
    languageSelect: null,
    emergencyKeywords: ['chest pain', 'heart attack', 'stroke', 'bleeding severely', 'unconscious', 'can\'t breathe'],

    init() {
        this.sessionId = this.generateUUID();
        this.chatWindow = document.getElementById('chat-window');
        this.inputField = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.languageSelect = document.getElementById('language-select');

        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    },

    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },

    checkEmergency(message) {
        const lowerMsg = message.toLowerCase();
        for (let keyword of this.emergencyKeywords) {
            if (lowerMsg.includes(keyword)) {
                if (window.UI) window.UI.showEmergencyBanner();
                this.logEmergency(message, keyword);
                return true;
            }
        }
        return false;
    },

    async logEmergency(message, keyword) {
        try {
            await fetch('/api/emergency/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    trigger_words: keyword,
                    message: message
                })
            });
        } catch (e) {
            console.error("Failed to log emergency");
        }
    },

    appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const avatar = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        msgDiv.innerHTML = `
            <div class="avatar">${avatar}</div>
            <div class="bubble">${this.formatText(text)}</div>
        `;
        
        this.chatWindow.appendChild(msgDiv);
        this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
    },

    formatText(text) {
        // Improved markdown parsing for bold and line breaks
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                   .replace(/\n/g, '<br>');
    },

    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message system typing-msg';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="avatar"><i class="fas fa-robot"></i></div>
            <div class="bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        this.chatWindow.appendChild(typingDiv);
        this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
    },

    removeTyping() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) typingDiv.remove();
    },

    async sendMessage() {
        const message = this.inputField.value.trim();
        if (!message) return;

        this.appendMessage('user', message);
        this.inputField.value = '';
        
        this.checkEmergency(message);
        this.showTyping();

        try {
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                    language: this.languageSelect.value
                })
            });

            this.removeTyping();
            
            // Create a new empty message bubble for streaming
            const msgDiv = document.createElement('div');
            msgDiv.className = `message system`;
            msgDiv.innerHTML = `
                <div class="avatar"><i class="fas fa-robot"></i></div>
                <div class="bubble"><span class="content"></span></div>
            `;
            this.chatWindow.appendChild(msgDiv);
            const contentSpan = msgDiv.querySelector('.content');

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let fullText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                fullText += decoder.decode(value, { stream: true });
                contentSpan.innerHTML = this.formatText(fullText);
                this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
            }
            
            if (window.Voice) window.Voice.speak(fullText);

        } catch (error) {
            this.removeTyping();
            this.appendMessage('system', 'Connection error. Please try again.');
        }
    }
};

window.Chatbot = Chatbot;
document.addEventListener('DOMContentLoaded', () => Chatbot.init());

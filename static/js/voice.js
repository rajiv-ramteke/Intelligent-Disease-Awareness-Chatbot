const Voice = {
    recognition: null,
    isRecording: false,
    micBtn: null,
    inputField: null,
    synthesis: window.speechSynthesis,

    init() {
        this.micBtn = document.getElementById('mic-btn');
        this.inputField = document.getElementById('chat-input');

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;

            this.recognition.onstart = () => {
                this.isRecording = true;
                this.micBtn.classList.add('mic-active');
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.inputField.value = transcript;
                // Automatically send message if Chatbot is available
                if (window.Chatbot) window.Chatbot.sendMessage();
            };

            this.recognition.onerror = (event) => {
                console.error("Speech recognition error", event.error);
                this.stopRecording();
            };

            this.recognition.onend = () => {
                this.stopRecording();
            };

            this.micBtn.addEventListener('click', () => this.toggleRecording());
        } else {
            this.micBtn.style.display = 'none'; // Hide if not supported
        }
    },

    toggleRecording() {
        if (this.isRecording) {
            this.recognition.stop();
        } else {
            this.recognition.lang = 'en-US';
            this.recognition.start();
        }
    },

    stopRecording() {
        this.isRecording = false;
        this.micBtn.classList.remove('mic-active');
    },

    speak(text) {
        if (!this.synthesis) return;
        
        // Remove markdown and disclaimers for cleaner speech if necessary
        const cleanText = text.replace(/\*\*/g, '');
        
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = 'en-US';
        
        this.synthesis.speak(utterance);
    }
};

document.addEventListener('DOMContentLoaded', () => Voice.init());

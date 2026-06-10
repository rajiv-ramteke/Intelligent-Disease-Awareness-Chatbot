/**
 * widgets.js – Health Tips Carousel, Suggested Questions, Health Categories
 * Handles all interactivity for the right-side widgets panel.
 */

const Widgets = {
    currentTip: 0,
    tips: [
        "Drink at least 8 glasses of water every day to stay hydrated and keep your body functioning well.",
        "Exercise for at least 30 minutes a day — even a brisk walk can significantly improve your health.",
        "Get 7–9 hours of quality sleep each night. Good sleep boosts immunity and mental health.",
        "Eat a rainbow of fruits and vegetables daily for a wide range of vitamins and antioxidants.",
        "Wash your hands frequently for at least 20 seconds to prevent the spread of germs and infections.",
        "Avoid smoking and limit alcohol consumption to reduce your risk of cancer, heart disease, and liver damage.",
        "Manage stress with deep breathing, meditation, or yoga. Chronic stress weakens your immune system.",
        "Get regular health check-ups and screenings, even when you feel healthy. Prevention is better than cure.",
        "Limit processed foods, sugary drinks, and excess salt. Prefer home-cooked, balanced meals.",
        "Maintain a healthy weight through a balanced diet and regular physical activity."
    ],

    allQuestions: [
        "What causes diabetes?",
        "Best foods for immunity?",
        "How to lose weight safely?",
        "Home remedies for cold and cough?",
        "What is hypertension and how to manage it?",
        "How to improve mental health?",
        "What are the symptoms of dengue?",
        "How much water should I drink daily?",
        "What is the best diet for heart health?",
        "How to prevent vitamin D deficiency?",
        "What are the signs of a stroke?",
        "How to reduce cholesterol naturally?"
    ],

    showingAll: false,
    showingAllCategories: false,

    init() {
        this.renderDots();
        this.updateTip();
        this.bindEvents();
    },

    renderDots() {
        const dotsContainer = document.getElementById('tip-dots');
        if (!dotsContainer) return;
        dotsContainer.innerHTML = '';
        this.tips.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.className = 'tip-dot' + (i === 0 ? ' active' : '');
            dot.addEventListener('click', () => this.goToTip(i));
            dotsContainer.appendChild(dot);
        });
    },

    updateTip() {
        const tipText = document.getElementById('tip-text');
        if (!tipText) return;

        // Fade out
        tipText.style.opacity = '0';
        tipText.style.transform = 'translateY(6px)';

        setTimeout(() => {
            tipText.textContent = this.tips[this.currentTip];
            tipText.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            tipText.style.opacity = '1';
            tipText.style.transform = 'translateY(0)';
        }, 200);

        // Update dots
        document.querySelectorAll('.tip-dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === this.currentTip);
        });
    },

    goToTip(index) {
        this.currentTip = (index + this.tips.length) % this.tips.length;
        this.updateTip();
    },

    bindEvents() {
        // Tip Navigation
        const prevBtn = document.getElementById('tip-prev');
        const nextBtn = document.getElementById('tip-next');
        if (prevBtn) prevBtn.addEventListener('click', () => this.goToTip(this.currentTip - 1));
        if (nextBtn) nextBtn.addEventListener('click', () => this.goToTip(this.currentTip + 1));

        // Auto-advance tips every 8 seconds
        setInterval(() => this.goToTip(this.currentTip + 1), 8000);

        // Suggested Questions – click to send message
        document.querySelectorAll('.suggested-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.getAttribute('data-q');
                this.sendToChat(question);
            });
        });

        // Health Category buttons
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.getAttribute('data-q');
                this.sendToChat(question);
            });
        });

        // View All Questions
        const viewAllQuestions = document.getElementById('view-all-questions');
        if (viewAllQuestions) {
            viewAllQuestions.addEventListener('click', () => {
                const list = document.getElementById('suggested-list');
                if (!list) return;
                this.showingAll = !this.showingAll;
                list.innerHTML = '';
                const questionsToShow = this.showingAll ? this.allQuestions : this.allQuestions.slice(0, 5);
                questionsToShow.forEach(q => {
                    const li = document.createElement('li');
                    li.innerHTML = `<button class="suggested-btn" data-q="${q}">${q}</button>`;
                    li.querySelector('.suggested-btn').addEventListener('click', () => this.sendToChat(q));
                    list.appendChild(li);
                });
                viewAllQuestions.innerHTML = this.showingAll
                    ? 'Show Less <i class="fas fa-chevron-up"></i>'
                    : 'View All <i class="fas fa-arrow-right"></i>';
            });
        }
    },

    sendToChat(question) {
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        if (input && sendBtn) {
            input.value = question;
            input.focus();
            // Trigger send
            sendBtn.click();
        }
    }
};

window.Widgets = Widgets;
document.addEventListener('DOMContentLoaded', () => Widgets.init());

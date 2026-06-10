const UI = {
    init() {
        this.navFacilities = document.getElementById('nav-facilities');
        this.navTips = document.getElementById('nav-tips');
        this.navChat = document.getElementById('nav-chat');
        this.widgetsPanel = document.getElementById('widgets-panel');
        this.mapsSubpanel = document.getElementById('maps-subpanel');
        this.healthWidgets = document.getElementById('health-widgets');
        this.closePanelBtn = document.getElementById('close-panel');

        this.bindEvents();
    },

    bindEvents() {
        if (this.navFacilities) {
            this.navFacilities.addEventListener('click', (e) => {
                e.preventDefault();
                this.showMapsPanel('Nearby Facilities');
                if (window.Maps) window.Maps.loadNearby();
                this.setActiveNav(this.navFacilities.parentElement);
            });
        }

        if (this.navTips) {
            this.navTips.addEventListener('click', (e) => {
                e.preventDefault();
                // Scroll the health widgets into view and highlight tip card
                this.showWidgets();
                const tipCard = document.querySelector('.tip-card');
                if (tipCard) {
                    tipCard.scrollIntoView({ behavior: 'smooth' });
                    tipCard.style.boxShadow = '0 0 0 2px #10B981';
                    setTimeout(() => { tipCard.style.boxShadow = ''; }, 1500);
                }
                this.setActiveNav(this.navTips.parentElement);
            });
        }

        if (this.navChat) {
            this.navChat.addEventListener('click', (e) => {
                e.preventDefault();
                this.showWidgets();
                this.setActiveNav(this.navChat.parentElement);
            });
        }

        if (this.closePanelBtn) {
            this.closePanelBtn.addEventListener('click', () => {
                this.showWidgets();
                this.setActiveNav(this.navChat ? this.navChat.parentElement : null);
            });
        }
    },

    setActiveNav(liElement) {
        document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
        if (liElement) liElement.classList.add('active');
    },

    showMapsPanel(title) {
        document.getElementById('panel-title').innerText = title;
        if (this.mapsSubpanel) this.mapsSubpanel.classList.remove('hidden');
        if (this.healthWidgets) this.healthWidgets.classList.add('hidden');
    },

    showWidgets() {
        if (this.mapsSubpanel) this.mapsSubpanel.classList.add('hidden');
        if (this.healthWidgets) this.healthWidgets.classList.remove('hidden');
    },

    showEmergencyBanner() {
        document.getElementById('emergency-banner').classList.remove('hidden');
    }
};

document.addEventListener('DOMContentLoaded', () => UI.init());

const Maps = {
    loadNearby(facilityType = 'hospitals', label = 'Hospitals') {
        const content = document.getElementById('panel-content');
        content.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 2rem;"><i class="fas fa-spinner fa-spin"></i> Locating you...</p>';

        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => this.showFacilityPanel(position.coords.latitude, position.coords.longitude, facilityType, label),
                () => this.showFacilityPanel(null, null, facilityType, label)
            );
        } else {
            this.showFacilityPanel(null, null, facilityType, label);
        }
    },

    showFacilityPanel(lat, lng, type = 'hospitals', label = 'Hospitals') {
        const content = document.getElementById('panel-content');

        let mapsUrl;
        if (lat && lng) {
            mapsUrl = `https://www.google.com/maps/search/${type}/@${lat},${lng},14z`;
        } else {
            mapsUrl = `https://www.google.com/maps/search/${type}+near+me/`;
        }

        const iconMap = {
            'hospitals':   'fa-hospital',
            'pharmacy':    'fa-pills',
            'blood+bank':  'fa-tint',
            'clinic':      'fa-stethoscope',
            'doctor':      'fa-user-md'
        };
        const colorMap = {
            'hospitals':   '#10B981',
            'pharmacy':    '#F59E0B',
            'blood+bank':  '#EF4444',
            'clinic':      '#3B82F6',
            'doctor':      '#8B5CF6'
        };
        const icon = iconMap[type] || 'fa-map-marker-alt';
        const color = colorMap[type] || 'var(--secondary)';

        content.innerHTML = `
            <div style="text-align: center; padding: 1.5rem 0.5rem;">
                <div style="
                    width: 70px; height: 70px;
                    border-radius: 50%;
                    background: ${color}22;
                    border: 2px solid ${color}55;
                    display: flex; align-items: center; justify-content: center;
                    margin: 0 auto 1rem;
                    font-size: 1.8rem; color: ${color};
                ">
                    <i class="fas ${icon}"></i>
                </div>
                <h4 style="margin-bottom: 0.5rem; font-size: 1.1rem; font-family: 'Outfit', sans-serif;">Find ${label}</h4>
                <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1.5rem; line-height: 1.6;">
                    ${lat ? 'Using your current location to find nearby ' + label.toLowerCase() + '.' : 'Searching for ' + label.toLowerCase() + ' near you.'}
                </p>
                <a href="${mapsUrl}" target="_blank" rel="noopener" style="
                    display: inline-flex; align-items: center; gap: 8px;
                    background: ${color};
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 700;
                    font-size: 0.85rem;
                    box-shadow: 0 4px 12px ${color}44;
                    transition: all 0.2s;
                ">
                    <i class="fas fa-external-link-alt"></i>
                    Open in Google Maps
                </a>
            </div>
        `;
    }
};

window.Maps = Maps;

document.addEventListener('DOMContentLoaded', () => {
    // Emergency banner -> hospitals
    const emergencyBtn = document.getElementById('find-hospitals-btn');
    if (emergencyBtn) {
        emergencyBtn.addEventListener('click', () => {
            document.getElementById('emergency-banner').classList.add('hidden');
            if (window.UI) window.UI.showMapsPanel('Nearby Emergency Hospitals');
            Maps.loadNearby('hospitals', 'Hospitals');
        });
    }

    // Facility type quick buttons in sidebar
    document.querySelectorAll('.facility-type-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-type');
            const label = btn.getAttribute('data-label');

            // Highlight active button
            document.querySelectorAll('.facility-type-btn').forEach(b => b.classList.remove('active-type'));
            btn.classList.add('active-type');

            // Show maps panel
            if (window.UI) window.UI.showMapsPanel(label);
            Maps.loadNearby(type, label);
        });
    });
});

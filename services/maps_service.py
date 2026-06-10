import requests
from config import Config

def get_nearby_places(lat, lng, facility_type):
    api_key = Config.GOOGLE_MAPS_API_KEY
    if not api_key or api_key == 'your_google_maps_api_key_here':
        # Mock data for demonstration if no API key is provided
        return [
            {
                "name": f"City General {facility_type.capitalize()}",
                "vicinity": "123 Health Ave, City",
                "rating": 4.5,
                "geometry": {"location": {"lat": float(lat) + 0.01, "lng": float(lng) + 0.01}}
            },
            {
                "name": f"Sunrise {facility_type.capitalize()}",
                "vicinity": "456 Wellness Blvd, City",
                "rating": 4.2,
                "geometry": {"location": {"lat": float(lat) - 0.01, "lng": float(lng) - 0.01}}
            }
        ]

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type={facility_type}&key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') == 'OK':
            return data.get('results', [])
        else:
            print(f"Google Maps API Error: {data.get('status')}")
            return []
    except Exception as e:
        print(f"Error fetching nearby places: {e}")
        return []

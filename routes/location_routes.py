from flask import Blueprint, request, jsonify
from services.maps_service import get_nearby_places

location_bp = Blueprint('location', __name__, url_prefix='/api/location')

@location_bp.route('/nearby', methods=['GET'])
def nearby_facilities():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    facility_type = request.args.get('type', 'hospital') # hospital, pharmacy, doctor

    if not lat or not lng:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    facilities = get_nearby_places(lat, lng, facility_type)
    return jsonify({"facilities": facilities})

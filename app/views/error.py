
from flask import jsonify

def handle_error(e, request):
    route_name = request.url_rule.rule
    print(f"Error in route {route_name}: {e}")
    return jsonify({
        'status': 'error',
        'message': 'An error occurred'
    }), 500
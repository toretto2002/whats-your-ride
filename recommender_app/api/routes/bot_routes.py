from flask import Blueprint, request, jsonify
from recommender_app.services.bot_service import BotService
from flask_jwt_extended import jwt_required

bot_service = BotService()
bp = Blueprint("bot_routes", __name__)


@bp.route('/bot', methods=['POST'])
@jwt_required()
def handle_bot_request():
    data = request.get_json()
    response = bot_service.handle_bot_request(data)
    return jsonify(response), 200

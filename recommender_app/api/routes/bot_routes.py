from flask import Blueprint, request, jsonify
from recommender_app.services.bot_service import BotService
from flask_jwt_extended import jwt_required

bot_service = BotService()
bp = Blueprint("bot_routes", __name__)


@bp.route('/bot', methods=['POST'])
@jwt_required()
def handle_bot_request():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Messaggio mancante"}), 400

    try:
        response = bot_service.ask(message)
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

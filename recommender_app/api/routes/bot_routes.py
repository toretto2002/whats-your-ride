from flask import Blueprint, request, jsonify
from recommender_app.services.bot_service import BotService
from flask_jwt_extended import jwt_required
# TEMPORANEAMENTE DISABILITATO: servizio deprecato
# from recommender_app.services.open_ai_bot_service import OpenAiBotService
from recommender_app.services.moto_it_open_ai_service import MotoItOpenAiBotService

bot_service = BotService()
# open_ai_bot_service = OpenAiBotService()  # DEPRECATO - causa NotImplementedError
moto_it_open_ai_bot_service = MotoItOpenAiBotService()  
bp = Blueprint("bot_routes", __name__)


@bp.route('/bot', methods=['POST'])
# @jwt_required()
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
    

@bp.route('/openai-bot', methods=['POST'])
# @jwt_required()
def handle_openai_bot_request():
    """ENDPOINT DEPRECATO - OpenAiBotService solleva NotImplementedError."""
    return jsonify({"error": "Endpoint deprecato, usa /moto-it-bot"}), 410


@bp.route('/moto-it-bot', methods=['POST'])
# @jwt_required()
async def handle_moto_it_bot_request():
    data = request.get_json()
    message = data.get("message")
    session_id = data.get("session_id")  # parametro opzionale
    comparison_ids = data.get("comparison_ids")  # parametro opzionale

    if not message:
        return jsonify({"error": "Messaggio mancante"}), 400
    
    try:
        raw_response = await moto_it_open_ai_bot_service.ask(message, session_id=session_id, comparison_ids=comparison_ids)
        formatted = _format_moto_it_response(raw_response)
        if formatted.get("error"):
            return jsonify(formatted), 500
        return jsonify(formatted)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _format_moto_it_response(raw: dict) -> dict:
    """
    Punto centrale dove si decide la struttura dell'oggetto JSON restituito dalla rotta /moto-it-bot.
    Adatta qui il payload finale indipendentemente da cosa ritorna il service.
    """
    if raw is None:
        return {"error": "Empty service response"}
    return {
        "session_id": raw.get("session_id"),
        "answer": raw.get("answer"),
        "sql_query": raw.get("sql_query"),
        "agent": raw.get("agent"),          # opzionale: quale agente ha risposto
        "reasoning": raw.get("reasoning"),  # opzionale: spiegazione interna
        "metadata": raw.get("metadata", {}),
        "error": raw.get("error"),
        "rows": raw.get("rows", [])  # opzionale: risultati della query SQL
    }

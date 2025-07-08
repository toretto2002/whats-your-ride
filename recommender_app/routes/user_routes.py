from flask import Blueprint, request, jsonify
from recommender_app.services.user_service import UserService
from recommender_app.schemas.registration_dto import UserRegistration, UserOut, UserUpdate

user_service = UserService()
bp = Blueprint("user_routes", __name__)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_in = UserRegistration(**data)
    user_out = user_service.create_user(user_in)
    return jsonify(user_out.model_dump(mode="json")), 201

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_out = user_service.get_user_by_id(user_id)
    if user_out:
        return jsonify(user_out.model_dump(mode="json")), 200
    return jsonify({"error": "User not found"}), 404

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user_update = UserUpdate(**data)
    user_out = user_service.update_user(user_id, user_update)
    return jsonify(user_out.model_dump(mode="json")), 200

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_service.delete_user(user_id)
    return jsonify({"message": "User deleted successfully"}), 204

@bp.route('/users', methods=['GET'])
def list_users():
    users = user_service.list_users()
    return jsonify([user.model_dump(mode="json") for user in users]), 200

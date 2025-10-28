from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from recommender_app.services.auth_service import AuthService

bp = Blueprint("auth_routes", __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = AuthService.login_user(username, password)
    if not user:
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    
    response = {
        "success": True,
        "data": {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.username,
                "role": user.role
            },
            "token": access_token,
            "refreshToken": None,  # Implement refresh token logic if needed
            "expiresIn": 3600  # Example expiration time in seconds 
        }
    }
    
    return jsonify(response), 200

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print(f"Current user: {current_user}")
    return jsonify(logged_in_as=current_user), 200

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Invalidate the token by not returning it
    return jsonify(msg="Successfully logged out"), 200

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token), 200 


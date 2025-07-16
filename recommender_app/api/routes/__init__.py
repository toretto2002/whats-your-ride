from .user_routes import bp as user_routes
from .auth_routes import bp as auth_routes
from .bot_routes import bp as bot_routes

blueprints = [user_routes, auth_routes, bot_routes]

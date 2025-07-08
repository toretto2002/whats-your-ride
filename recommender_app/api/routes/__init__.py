from .user_routes import bp as user_routes
from .auth_routes import bp as auth_routes

blueprints = [user_routes, auth_routes]

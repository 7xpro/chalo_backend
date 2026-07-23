from flask import Blueprint

from app.controllers.user_controller import user_controller

user_bp = Blueprint('user', __name__)
user_bp.post('/create',)(user_controller.create_user)
user_bp.post ('/login',)(user_controller.login_user)
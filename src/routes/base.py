from flask import Blueprint, request, jsonify, render_template
from src.views import base
from src.utils.ext import oneid
from flask_login import current_user

base_router = Blueprint('base_route', __name__)

@base_router.route('/')
def home():
    print(current_user.is_authenticated)
    return base.home_controller()

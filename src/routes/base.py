from flask import Blueprint, request, jsonify
from src.views import base
from src.utils.ext import oneid


base_router = Blueprint('base_route', __name__)

@base_router.route('/')
def home():
    return base.home_controller()

# @base_route.route("/oneid/login")
# def oneid_login():
#     return 'hello'

# @base_route.route("/params", methods=['GET'])
# def params():
#     data = oneid.Params_To_Dict(request.args)
#     return jsonify(data)

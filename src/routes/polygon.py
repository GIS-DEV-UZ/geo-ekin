from flask import Blueprint, request, redirect, url_for, jsonify
from flask_login import current_user
import json, os

# from src.views import user
# from flask_login import current_user, login_user, login_required, logout_user
# from src.utils.ext import oneid, db
from src.models.polygon import Polygon

# from src.models.user import User

polygon_router = Blueprint("polygon_route", __name__, url_prefix="/")


@polygon_router.route("/save_polygon/<cadastral_number>", methods=["GET", "POST"])
def save_polygon(cadastral_number):
    polygon = Polygon.query.filter_by(cad_number=cadastral_number).first()
    if polygon:
        if polygon.user_id != current_user.id:
            polygon = Polygon(cad_number=cadastral_number, user_id=current_user.id)
            polygon.save()
            return jsonify({"success": True})
        else:
            return jsonify("uje bor")
    else:
        polygon = Polygon(cad_number=cadastral_number, user_id=current_user.id)
        polygon.save()
        return jsonify({"success": True})


@polygon_router.route("/get_polygons/<user_id>", methods=["GET", "POST"])
def get_polygons(user_id):
    polygon_list = Polygon.query.filter_by(user_id=int(user_id)).all()
    polygon_cad_numbers = []
    for polygon in polygon_list:
        polygon_cad_numbers.append(polygon.cad_number)

    return jsonify({"polygon_cad_number": polygon_cad_numbers})

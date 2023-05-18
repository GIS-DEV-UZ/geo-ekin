from flask import Blueprint, request, redirect, json
from src.views import user
from flask_login import current_user, login_user, login_required, logout_user
from src.utils.ext import oneid, db
from src.models.user import User
from src.models.polygon import Polygon
from src.views.user import user_polygon_info_temp

import pprint
user_route = Blueprint("user_route", __name__, url_prefix="/user")


@user_route.route("/params", methods=["GET"])
def get_params():
    data = oneid.Params_To_Dict(request.args)
    pprint.pprint(data)
    user_req = User.query.filter_by(user_id=data["user_id"]).first()
    if user_req:
        login_user(user_req)
    else:
        user = User(
            user_id=data["user_id"],
            first_name=data["first_name"],
            last_name=data["sur_name"],
            full_name=data["full_name"],
            passport=data["pport_no"],
            oneid_user_id=data["user_id"],
            pinfl=data["pin"],
            email=data["email"],
            phone_number=data["mob_phone_no"],
        )
        user.create()
        login_user(user)
    return redirect("/")


@user_route.route("/profile")
@login_required
def user_profile():
    return user.user_profile_controller()


@user_route.route("/polygon")
def user_polygon():
    cad_number = request.args.get("cad_number")
    return user.user_map(cad_number)


@user_route.route("/polygon/all")
def polygon_all():
    user_id = current_user.id
    polygon_list = Polygon.query.filter_by(user_id=int(user_id)).all()
    polygon_cad_number = []

    for polygon in polygon_list:
        polygon_cad_number.append(polygon.cad_number)

    return user.all_polygons(json.dumps(polygon_cad_number))

@user_route.route("/polygon/info")
def user_polygon_info():
    return user_polygon_info_temp()
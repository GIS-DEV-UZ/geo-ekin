from flask import Blueprint, request, redirect, url_for, jsonify
from flask_login import current_user
import json, os
from psycopg2 import connect


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

@polygon_router.route("/get_contours/", methods=["GET", "POST"])
def get_contours():
    cadastral_number = request.args.get('cadastral_number')

    if cadastral_number is None:
        return jsonify({
            'msg': "Error: cadastral number not defined"
        }), 400
    

   
    connection = connect(
        database = 'cropplacement',
        user = 'odya',
        password = 'o030101',
        host = '127.0.0.1',
        port = 5433
    )
    cursor = connection.cursor()



    query = f"""
        SELECT jsonb_build_object(
            'type',     'FeatureCollection',
            'features', jsonb_agg(features.feature)
        )
        FROM (
        SELECT jsonb_build_object(
            'type',       'Feature',
            'id',         id,
            'geometry',   ST_AsGeoJSON(geometry)::jsonb,
            'properties', to_jsonb(inputs) - 'id' - 'geometry'
        ) AS feature
        FROM (SELECT id, contour_number, farm_cad_number, area, geometry FROM crop_placement where farm_cad_number = '{cadastral_number}') inputs) features;

    
    """
    cursor.execute(query)

    contours = cursor.fetchone()[0]


    return jsonify({'data': contours})


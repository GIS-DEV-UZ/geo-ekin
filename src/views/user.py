from flask import render_template



def user_profile_controller():
    return render_template('profile.html')

def user_map(cad_number):
    return render_template('map_one.html', cad_number = cad_number)

def all_polygons(polygon_cad_number):
    return render_template('map.html', polygon_cad_number = polygon_cad_number)

def user_polygon_info_temp():
    return render_template('user_polygon_info.html')

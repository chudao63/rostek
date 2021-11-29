from app import app, api
from flask import send_from_directory, render_template
from flask_fontawesome import FontAwesome
from .apis import *

FontAwesome(app)

@app.route('/js/<path:path>')
def js(path):
    return send_from_directory("dev/templates/static/assets/js/", path)

@app.route('/css/<path:path>')
def css(path):
    return send_from_directory("dev/templates/static/assets/css/", path)

# @app.route('/fonts/<path:path>')
# def font(path):
#     return send_from_directory("dev/templates/static/assets/fonts/", path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("dev/templates/static/assets/img/", 'favicon.ico')

@app.route('/postman')
def postman():
    return render_template('dev/AgvMonitor.postman_collection.json')

@app.route('/dev')
def dev():
    return render_template('dev/templates/index/index.html')

api.add_resource(
    FrontendTestApi, 
    '/agv1',
    '/agv2',
    '/agv3',
    '/agv4',
    '/agv5',
    '/agv6',
    '/agv7',
    '/agv8',
    '/agv9',
)
api.add_resource(
    NotifyApi, 
    '/notify_sucess',
    '/notify_error',
)

api.add_resource(
   FrontendIntersectApi, 
    '/intersect_0',
    '/intersect_1',
    '/intersect_2',
    '/intersect_3',
)

api.add_resource(
   BackendTestApi, 
    '/backend/test',
)

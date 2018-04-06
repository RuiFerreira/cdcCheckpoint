from models.base import Session, engine, Base
from models.POI import poi
from models.prediction import prediction
from models.Camera import camera
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, jsonify, request
from collections import OrderedDict
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from dbmanager import insertPOI, insertCamera, insertPrediction
import datetime

#definicao da app
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres@localhost/cdcv2'
app.debug=True 
CORS(app, resources=r'/*', allow_headers=['Origin', 'Content-Type', 'Accept', 'Authorization', 'X-Request-With'], supports_credentials=True)


#abre sessao para coneccao a BD
session = Session()
#criacao de objeto marshmallow
ma=Marshmallow(app)

#schemas para conversao de dados para jason sem erros
class POISchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'POIName', 'geoLat', 'geoLong', 'active')

poi_schema = POISchema()
poi_schema = POISchema(many=True)

class CameraSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'IPaddress', 'POI_id', 'active')

camera_schema = CameraSchema()
camera_schema = CameraSchema(many=True)

class PredictionSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'Prediction', 'Camera_id', 'Time', 'latest')

prediction_schema = PredictionSchema()
prediction_schema = PredictionSchema(many=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/', methods=['GET'])
def helloworld():
    return 'hello world'

#READ
#poi - all data
@app.route('/pois', methods =['GET'])
def get_pois():
    allPOIs = session.query(poi).filter(True == poi.active)
    result=poi_schema.dump(allPOIs)
    return jsonify(result.data)
#poi - all data
@app.route('/cameras', methods =['GET'])
def get_cameras():
    allCameras = session.query(camera).filter(True == camera.active)
    result=camera_schema.dump(allCameras)
    return jsonify(result.data)
#poi - all data
@app.route('/predictions', methods =['GET'])
def get_predictions():
    allPredictions = session.query(prediction).filter(True == prediction.latest)
    result=prediction_schema.dump(allPredictions)
    return jsonify(result.data)

#Create
#pois - add poi
@app.route('/pois/add', methods =['POST'])
def post_poi():
    req_data= request.get_json()
    POIName = req_data['POIName']
    geoLat =  req_data['geoLat']
    geoLong = req_data['geoLong']
    insertPOI(POIName, geoLat, geoLong)
    return 'Success'

#cameras - add camera
@app.route('/cameras/add', methods =['POST'])
def post_camera():
    req_data= request.get_json()
    ip_address = req_data['IPaddress']
    poi_id =  req_data['POI_id']
    insertCamera(ip_address, poi_id)
    return 'Success'

#predicitions - add prediction
@app.route('/predictions/add', methods =['POST'])
def post_prediction():
    req_data= request.get_json()
    predictToAdd = req_data['Prediction']
    camera_id =  req_data['Camera_id']
    insertPrediction(predictToAdd, camera_id)
    return 'Success'

#poi - findByID
@app.route('/pois/description', methods =['GET'])
def get_poi_by_id():
    poi_id = request.args.get('arg')
    singlePOI = session.query(poi).filter(poi_id == poi.id and True==poi.active)
    result=poi_schema.dump(singlePOI)
    return jsonify(result.data)

#camera - findByID
@app.route('/cameras/description', methods =['GET'])
def get_camera_by_id():
    camera_id = request.args.get('arg')
    singleCamera = session.query(camera).filter(camera_id == camera.id and True==camera.active)
    result=camera_schema.dump(singleCamera)
    return jsonify(result.data)

#prediction - findByID
@app.route('/predictions/description', methods =['GET'])
def get_prediction_by_id():
    prediction_id = request.args.get('arg')
    singlePrediction = session.query(prediction).filter(prediction_id == prediction.id and True==prediction.latest)
    result=prediction_schema.dump(singlePrediction)
    return jsonify(result.data)

#UPDATE
#pois - update poi 
@app.route('/pois/update', methods=['PUT'])
def update_poi():
    poi_id = request.args.get('arg')
    req_data= request.get_json()
    reqPOIName = req_data['POIName']
    reqgeoLat =  req_data['geoLat']
    reqgeoLong = req_data['geoLong']
    findByID = session.query(poi).filter(poi.id==poi_id and True==poi.active).first()
    findByID.POIName=reqPOIName
    findByID.geoLat= reqgeoLat
    findByID.geoLong= reqgeoLong
    session.commit()
    return 'success' 

#cameras - update camera
@app.route('/cameras/update', methods=['PUT'])
def update_camera():
    camera_id = request.args.get('arg')
    req_data = request.get_json()
    reqIPaddress = req_data['IPaddress']
    reqPOIid = req_data['POI_id']
    findByID = session.query(camera).filter(camera.id==camera_id and True==camera.active).first()
    findByID.IPaddress =reqIPaddress
    findByID.POI_id = reqPOIid
    session.commit()
    return 'success'

#predictions - update prediction
@app.route('/predictions/update', methods=['PUT'])
def update_prediction():
    prediction_id = request.args.get('arg')
    req_data = request.get_json()
    reqCameraID= req_data['Camera_id']
    reqPrediction = req_data['Prediction']
    findByID = session.query(prediction).filter(prediction.id == prediction_id and True==prediction.latest).first()
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    findByID.Camera_id = reqCameraID
    findByID.Prediction = reqPrediction
    findByID.Time = timestamp
    return 'success'
    
#DELETE
#pois - delete poi by id
@app.route('/pois/delete', methods=['DELETE'])
def del_poi():
    poi_id = request.args.get('arg')
    poiToDelete = session.query(poi).filter(poi.id==poi_id and True==poi.active).first()
    poiToDelete.active = False
    session.commit()
    return 'success'

#cameras - delete camera by id
@app.route('/cameras/delete', methods=['DELETE'])
def del_camera():
    camera_id = request.args.get('arg')
    cameraToDelete = session.query(camera).filter(camera.id==camera_id and True == camera.active).first()
    cameraToDelete.active = False
    session.commit()
    return 'success'

#predictions - delete prediction by id
@app.route('/predictions/delete', methods=['DELETE'])
def del_prediction():
    prediction_id = request.args.get('arg')
    predictionToDelete = session.query(prediction).filter(prediction.id==prediction_id and True == prediction.latest).first()
    predictionToDelete.latest = False
    session.commit()
    return 'success'

#Find Camera by IP - need to replace <ip> for arg ip
@app.route('/cameras/findbyip', methods=['GET'])
def findCameraByIP():
    ip = request.args.get('arg')
    allCameras = session.query(camera).filter((camera.IPaddress.contains(str(ip))) & (camera.active==True))
    result=camera_schema.dump(allCameras)
    return jsonify(result.data)

#Find POI by name - need to replace <name> for arg ip
@app.route('/pois/findbyname', methods=['GET'])
def findPOIByName():
    name = request.args.get('arg')
    allPOIs = session.query(poi).filter((poi.POIName.contains(str(name))) & (poi.active==True))
    result=poi_schema.dump(allPOIs)
    return jsonify(result.data)

if __name__=="__main__":
    app.run(threaded=True)
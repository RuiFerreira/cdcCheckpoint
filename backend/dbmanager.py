from models.Camera import camera
from models.base import Session, engine, Base
from models.POI import poi
from models.prediction import prediction
import datetime

Base.metadata.create_all(engine)

def insertPOI(poiname,geolat,geolong):
    session=Session()
    newPOI = poi(poiname,geolat,geolong)
    session.add(newPOI)
    session.commit()

def insertCamera(ip_address,poi_id):
    session=Session()
    newCamera = camera(ip_address,poi_id)
    session.add(newCamera)
    session.commit()

def insertPrediction(predict,id_camara):
    session=Session()
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    newPrediction = prediction(predict,id_camara,timestamp)
    session.add(newPrediction)
    session.commit()





    

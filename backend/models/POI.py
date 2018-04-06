from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, FLOAT

from models.base import Base

class poi(Base):
    __tablename__ = 'poi'

    id = Column(Integer, primary_key=True)
    POIName = Column(String(80))#sera que tem q ser unique
    geoLat = Column(FLOAT(50))#sera que tem q ser unique
    geoLong = Column(FLOAT(50))
    active = Column(Boolean, default=True)
    #open hours and close hours maybe

    def __init__(self, POIName, geoLat, geoLong):
        self.POIName = POIName
        self.geoLat = geoLat
        self.geoLong = geoLong
        self.active = True

    
    
    def __repr__(self):
        return '<POI %r>' % self.POIName





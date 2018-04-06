from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
import datetime
from models.base import Base




class prediction(Base):
    __tablename__ = 'prediction'

    id = Column(Integer, primary_key=True)
    Prediction = Column(Enum('low_density','medium_low_density','medium_density','medium_high_density','high_density', name='prediction_type'))
    Camera_id = Column(Integer, ForeignKey('camera.id'))
    #trocar pelo POI id??
    Time = Column(DateTime(timezone=True), default=func.now())
    latest = Column(Boolean, default=True)

    #open hours and close hours maybe
    def __init__(self, Prediction, Camera_id, Time):
        self.Prediction = Prediction
        self.Camera_id = Camera_id
        self.Time = Time
        self.latest = True
    def __repr__(self):
        return '<Prediction %r>' % self.Prediction
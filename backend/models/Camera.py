from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from models.base import Base

class camera(Base):
    __tablename__ = 'camera'

    id = Column(Integer, primary_key=True)
    IPaddress = Column(String(80))#sera que tem q ser unique
    active = Column(Boolean, default=True)
    POI_id = Column(Integer, ForeignKey('poi.id'))
    

    #open hours and close hours maybe

    def __init__(self, IPaddress, POI_id):
        self.IPaddress = IPaddress
        self.active = True
        self.POI_id = POI_id

    def __repr__(self):
        return '<Camera %r>' % self.IPaddress
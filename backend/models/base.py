from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

engine = create_engine('postgresql://postgres@localhost/cdcv2')
Session = sessionmaker(bind=engine)

Base = declarative_base()


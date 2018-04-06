from models.Camera import camera
from models.base import Session, engine, Base
from models.POI import poi
from models.prediction import prediction
import datetime

Base.metadata.create_all(engine)

session= Session()

praca = poi("praca", 4.124124124, 15.123123123)
avenida = poi("avenida", 4.154152324, 12.124562123)
museu = poi("museu", 4.124124124, 15.123123123)

session.add(praca)
session.add(avenida)
session.add(museu)

session.commit()

camera1 = camera("0.0.0.0",1)
camera2 = camera("1.1.1.1",2)
camera3 = camera("2.2.2.2",3)

session.add(camera1)
session.add(camera2)
session.add(camera3)

session.commit()
'''
prediction1 = prediction("low_density", 1)
prediction2 = prediction("medium_low_density", 2)
prediction3 = prediction("high_density", 3)
'''



prediction1 = prediction("low_density", 1, datetime.datetime.now(datetime.timezone.utc))
prediction2 = prediction("medium_low_density", 2, datetime.datetime.now(datetime.timezone.utc))
prediction3 = prediction("high_density", 3, datetime.datetime.now(datetime.timezone.utc))

session.add(prediction1)
session.add(prediction2)
session.add(prediction3)
#commit and close session
session.commit()
session.close()

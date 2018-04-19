import csv
import os
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker


from .app import DrWaterAllocation as app


csv_filename = "DiversionPointsESPG4326.csv"

def read_points_from_csv():
    folder_path = os.path.dirname(__file__)
    file_path = os.path.join(folder_path, csv_filename)

    diversion_points_csv = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            point = (row['DESCRIPCIO'],float(row['Q_m3_s_D']),float(row['POINT_X']),float(row['POINT_Y']))
            diversion_points_csv.append(point)
    return diversion_points_csv


Base = declarative_base()

#Definition for diversion point persistent store
class DiversionPoints(Base):

    __tablename__ = 'diversionPoints'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    demand = Column(Float)
    priority = Column(Integer)
    efficiency = Column(Float)
    water_diverted = Column(Float)

class Dams(Base):

    __tablename__ = 'dam'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    output = Column(Float)

def init_main_db(engine, first_time):

    # Create all the tables
    Base.metadata.create_all(engine)

    #if first_time:
    Session = sessionmaker(bind=engine)
    session = Session()

    original_points = read_points_from_csv()

    for item in original_points:
        diversion_point = DiversionPoints(
            latitude=item[2],
            longitude=item[3],
            name=item[0],
            demand=item[1],
            priority=2,
            efficiency=.65,
            water_diverted=2
        )
        session.add(diversion_point)

    dam1 = Dams(
        name="habada",
        latitude=-71.05109,
        longitude=18.70798,
        output=100
    )

    dam2 = Dams(
        name="babada",
        latitude=-71.289964,
        longitude=18.9820202,
        output=100
    )
    session.add(dam1)
    session.add(dam2)
    session.commit()
    session.close()

def get_all_dams():
    """
    Get all persisted dams.
    """
    # Get connection/session to database
    Session = app.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()

    # Query for all dam records
    dams = session.query(Dams).all()
    session.close()

    return dams

def get_all_diversions():
    """
    Get all persisted diversions.
    """
    # Get connection/session to database
    Session = app.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()

    # Query for all dam records
    diversion_points = session.query(DiversionPoints).all()
    session.close()

    return diversion_points

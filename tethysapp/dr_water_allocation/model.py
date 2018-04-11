import csv
import os


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
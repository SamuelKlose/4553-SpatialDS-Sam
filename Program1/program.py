import pyqtree
import csv
from math import *
import numpy as np
import os
import time

def loadCities():
    citys = []
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'citylist.csv')
    with open(filename, 'rb') as csvfile:
        citysCsv = csv.reader(csvfile, delimiter=',', quotechar='"')
        for city in citysCsv:
            citys.append({"Name":city[0],"Country":city[1],"lat":city[2],"lon":city[3]})
    return citys


def displace(lat,lng,theta, distance,unit="miles"):
    """
    Displace a LatLng theta degrees clockwise and some feet in that direction.
    Notes:
        http://www.movable-type.co.uk/scripts/latlong.html
        0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
    Args:
        theta:    A number in degrees where:
                  0   = North
                  90  = East
                  180 = South
                  270 = West
        distance: A number in specified unit.
        unit:     enum("miles","kilometers")
    Returns:
        A new LatLng.
    """
    theta = np.float32(theta)
    radiusInMiles = 3959
    radiusInKilometers = 6371
    
    if unit == "miles":
        radius = radiusInMiles
    else:
        radius = radiusInKilometers

    delta = np.divide(np.float32(distance), np.float32(radius))

    theta = deg2rad(theta)
    lat1 = deg2rad(lat)
    lng1 = deg2rad(lng)

    lat2 = np.arcsin( np.sin(lat1) * np.cos(delta) +
                      np.cos(lat1) * np.sin(delta) * np.cos(theta) )

    lng2 = lng1 + np.arctan2( np.sin(theta) * np.sin(delta) * np.cos(lat1),
                              np.cos(delta) - np.sin(lat1) * np.sin(lat2))

    lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

    return [rad2deg(lat2), rad2deg(lng2)]

def deg2rad(theta):
        return np.divide(np.dot(theta, np.pi), np.float32(180.0))

def rad2deg(theta):
        return np.divide(np.dot(theta, np.float32(180.0)), np.pi)

def lat2canvas(lat):
    """
    Turn a latitude in the form [-90 , 90] to the form [0 , 180]
    """
    return float(lat) % 180

def lon2canvas(lon):
    """
    Turn a longitude in the form [-180 , 180] to the form [0 , 360]
    """
    return float(lon) % 360
    
def canvas2lat(lat): 
    """
    Turn a latitutude in the form [0 , 180] to the form [-90 , 90]
    """
    return ((float(lat)+90) % 180) - 90
    
def canvas2lon(lon):
    """
    Turn a longitude in the form [0 , 360] to the form [-180 , 180]
    """
    return ((float(lon)+180) % 360) - 180

def main():
    start_time = time.time()
    f = open('output.dat', 'w')
    f.write('Samuel Klose\n9/15/2015\nProgram 1 - Intro to Quadtrees\n============================================================================================\n')
    spindex = pyqtree.Index(bbox=[0, 0 , 360, 180])
    cities = loadCities()
    f.write('All cities within the bounding box: [45.011419, -111.071777 , 40.996484, -104.040527]:\n')
    for c in cities:
        #{'lat': '-18.01274', 'Country': 'Zimbabwe', 'lon': '31.07555', 'Name': 'Chitungwiza'}
        item = c['Name']
        bbox =[float(c['lat']),float(c['lon']),float(c['lat']),float(c['lon'])]
        spindex.insert(item=item, bbox=bbox)

    overlapbbox = (45.011419, -111.071777 , 40.996484, -104.040527)
    matches = spindex.intersect(overlapbbox)
    s = str(matches)
    f.write(s)
    f.write('\n============================================================================================\nAll cities within 500 miles of this point: (23.805450, -78.156738):\n')
    lat1 = 23.805450
    lon1 = -78.156738
    minX = displace(lat1, lon1, 270, 500)
    maxX = displace(lat1, lon1, 90, 500)
    minY = displace(lat1, lon1, 180, 500)
    maxY = displace(lat1, lon1, 0, 500)
    overlapbbox = (minY[0], minX[1], maxY[0], maxX[1])
    matches = spindex.intersect(overlapbbox)
    s = str(matches)
    f.write(s)
    f.write("Program ran in %s seconds." % (time.time() - start_time))
    f.close()

if __name__ == '__main__':
    main()

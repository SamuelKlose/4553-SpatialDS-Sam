"""
@author - Samuel Klose
@date -  11/17/15
@description - This program reads in nodes and edges from respective csv files and geometry
from a json file. The nodes and edges are stored in lists and a dictionary of the geometry
is created from the json file. Then the program prints out a random node's geometry
from the created dictionary.

@resources - I found code and methods in class.
"""
import csv
import json

nodes = [] #create an empty list to store nodes
edges = [] #create an empty list to store edges
geometry = {} #create an empty dictionary to store the geometry

with open('nodes.csv', 'rb') as csvfile: #open the nodes.csv file
    nodereader = csv.reader(csvfile, delimiter=',', quotechar='"') #create a reader
    for row in nodereader: #grab each row from the reader
        nodes.append(row) #add it to the list of nodes

with open('edges.csv', 'rb') as csvfile: #open the edges.csv file
    edgereader = csv.reader(csvfile, delimiter=',', quotechar='"') #create a reader
    for row in edgereader: #grab each row from the reader
        edges.append(row) #add it to the list of edges

f = open('nodegeometry.json', 'r') #open the json

for line in f:
    line = json.loads(line) #grab each line from the json
    geometry[line['id']] = line['geometry'] #add the geometry to the dictionary

print 'Sam Klose'
print 'Program 5 - Part 1'

print 'nodes.csv read containing %i nodes' % len(nodes)
print 'edges.csv read containing %i edges' % len(edges)

geo = json.loads(geometry[str(203981)]) #grab each point from the given line

print 'Node 203891 contains %i points. The geometry follows:' % len(geo)

for point in geo: #for each point
    print point #print


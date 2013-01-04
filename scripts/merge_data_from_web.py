"""
General purpose of this script is to add together a bunch of raw data
from the cycletracks database.  Since the web download likes it best 
when you only download a bunch of records at a time, this script puts
them back together into separate CSVs for trips, users, and data points
and does some summaries.

"""

__author__ = "elizabeth sall"
__email__  = "elizabeth@sfcta.org"
__date__   = "2013-01-03"

import sys, os

# Ugly work around for now

ADD_PATH = r"Q:\Model Research\CycleTracks\cycletracks"
sys.path.insert(0,ADD_PATH)

from cycletracks import CycletracksData

# Data which to import.  
# You can add lots to the list and it will all get added together.  
RAW_CYCLETRACKS_CSV_FILENAMES = ["testData/bikedata_test.csv"]

# Specify where to write out the separate CSVs, and what their prefix should be
SEPARATE_CSV_LOC    = r"Q:\Model Research\CycleTracks\Data"
SEPARATE_CSV_PREFIX = "JAN032013"

users_out = os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_USERS.csv")
trips_out = os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_TRIPS.csv")
points_out= os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_POINTS.csv")

d = CycletracksData()
for f in RAW_CYCLETRACKS_CSV_FILENAMES:
    d.addDataFromFile(f)

#print out a few records to make sure data got added correctly
for t in d.trips[2]:
    print t
for u in d.users[2]:
    print u
for p in d.points[0:10]:
    print p

(userfilename, tripsfilename, pointsfilename) = d.printToFile(SEPARATE_CSV_LOC, SEPARATE_CSV_PREFIX)



                
            


__copyright__ = "Copyright 2013 SFCTA"
__author__ = "elizabeth sall"
__email__  = "elizabeth@sfcta.org"
__date__   = "2013-01-03"
__license__   = """
This file is part of CycleTracks Crusher
CycleTracks Crusher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CycleTracks Crusher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CycleTracks Crusher.  If not, see <http://www.gnu.org/licenses/>.
"""


ABOUT ="""
General purpose of this script is to add together a bunch of raw data
from the cycletracks database.  Since the web download likes it best 
when you only download a bunch of records at a time, this script puts
them back together into separate CSVs for trips, users, and data points
and does some summaries.
"""

import sys, os

# Ugly work around for now

ADD_PATH = r"Q:\Model Research\CycleTracks\cycletracks"
sys.path.insert(0,ADD_PATH)

from cycletracks import CycletracksData

# Data which to import.  
# You can add lots to the list and it will all get added together.  
RAW_CYCLETRACKS_CSV_FILENAMES = [r"Q:/Model Research/CycleTracks/Data/bikedata_test.csv"]

RAW_CYCLETRACKS_CSV_FILENAMES = [r"Q:/Model Research/CycleTracks/Data/bikedata_1_5000.csv",
r"Q:/Model Research/CycleTracks/Data/bikedata_5001_10000.csv",
r"Q:/Model Research/CycleTracks/Data/bikedata_10001_15000.csv",
r"Q:/Model Research/CycleTracks/Data/bikedata_15001_20000.csv",
r"Q:/Model Research/CycleTracks/Data/bikedata_20001_25000.csv",
r"Q:/Model Research/CycleTracks/Data/bikedata_30001_35541.csv"]

TRIPS_ONLY = True
# Specify where to write out the separate CSVs, and what their prefix should be
SEPARATE_CSV_LOC    = r"Q:\Model Research\CycleTracks\Data"
SEPARATE_CSV_PREFIX = "JAN07_2013"

users_out = os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_USERS.csv")
trips_out = os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_TRIPS.csv")
points_out= os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_POINTS.csv")

d = CycletracksData()
for f in RAW_CYCLETRACKS_CSV_FILENAMES:
    d.addDataFromFile(f, tripsOnly= TRIPS_ONLY)

#print out a few records to make sure data got added correctly
for t in d.trips[:2]:
    print t
for u in d.users[:4]:
    print u
if TRIPS_ONLY:
    for p in d.points[:10]:
        print p

(userfilename, tripsfilename, pointsfilename) = d.printToFile(SEPARATE_CSV_LOC, SEPARATE_CSV_PREFIX, tripsOnly=TRIPS_ONLY)



                
            


import sys, os

ADD_PATH = r"Q:\Model Research\CycleTracks\cycletracks"
sys.path.insert(0,ADD_PATH)

from cycletracks import CycletracksData

#RAW_CYCLETRACKS_CSV_FILENAMES = [r"Q:\Model Research\CycleTracks\Data\bikedata_test.csv"]


RAW_CYCLETRACKS_CSV_FILENAMES = [r"Q:\Model Research\CycleTracks\Data\bikedata_1_5000.csv" ,
r"Q:\Model Research\CycleTracks\Data\bikedata_5001_10000.csv",
r"Q:\Model Research\CycleTracks\Data\bikedata_10001_15000.csv",
r"Q:\Model Research\CycleTracks\Data\bikedata_15001_20000.csv",
r"Q:\Model Research\CycleTracks\Data\bikedata_20001_25000.csv",
r"Q:\Model Research\CycleTracks\Data\bikedata_25001_30000.csv",
r"Q:\Model Research\CycleTracks\Data\bikedata_30001_35541.csv"]

# Specify where to write out the separate CSVs, and what their prefix should be
SEPARATE_CSV_LOC    = r"Q:\Model Research\CycleTracks\Data"
SEPARATE_CSV_PREFIX = "JAN032013"

users_out = os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_USERS.csv")
trips_out = os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_TRIPS.csv")
points_out= os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_POINTS.csv")

def concatenateFiles( fileList ):
    for (basefile, addfile) in fileList:
        f_add  = open(addfile, 'r')
        if os.path.isfile(basefile):
            f_orig = open(basefile, 'a')
            header = True
            for line in f_add:
                if not header:
                    f_orig.write(line)
                else:
                    header = False
        else:
            f_orig = open(basefile, 'w')
            for line in f_add:
                f_orig.write(line)
        print "Finished adding\n   %s\n to \n   %s" % (addfile, basefile)


d = CycletracksData()
for f in RAW_CYCLETRACKS_CSV_FILENAMES:
    d.addDataFromFile(f)

(userfilename, tripsfilename, pointsfilename) = d.printToFile(SEPARATE_CSV_LOC, SEPARATE_CSV_PREFIX)
    #concatenateFiles( [ (users_out, userfilename), (trips_out, tripsfilename), (points_out, pointsfilename) ] )

"""
UNCOMMENT TO TEST PRINT
    for t in d.trips:
        print t

    for u in d.users:
        print u

    for p in d.points[0:10]:
        print p
"""
    

                
            


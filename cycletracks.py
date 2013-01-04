import datetime, os


class CycletracksData(object):
    def __init__(self):
        self.files_to_recs     = {}
        self.trips             = []
        self.trips_by_id       = {}
        self.trips_by_user_id  = {}
        self.points            = []
        self.points_by_id      = {}
        self.points_by_trip_id = {}
        self.points_by_user_id = {}
        self.users        = []
        self.users_by_id  = {}


    def addDataFromFile(self, csvfilename):
        F = open(csvfilename, mode = 'r')
        inPoints = False
        inTrips  = False
        lines = 0
        points= 0
        trips = 0
        for line in F:
            lines += 1
            if not line.strip():
                inPoints = False
                inTrips  = False
            elif line[:5] == 'Found':
                pass
                ##todo add how many records found
            elif inPoints:
                self.readPoint(line)
                points += 1
            elif inTrips:
                self.readTrip(line)
                trips += 1
            elif line.strip().split(',')[-1] == 'recorded':
                inPoints = True
                print "reading points"
            elif line.strip().split(',')[-1] == 'purpose':
                inTrips = True
                print "reading trips"
            if lines % 100000 == 0:
                print "Read lines: %d trips: %d points: %d" % (lines, trips, points)
        print "TOTAL LINES: %d" % (lines)
        print "TOTAL TRIPS: %d" % (trips)
        print "TOTAL POINTS: %d" % (points)
    
    
    def readPoint(self, csvLine_point):
        (trip_id, lat, lon, alt, hAcc, vAcc, speed, dt) = csvLine_point.strip().split(",")
        
        trip_id = int(trip_id)
        lat     = float(lat)
        lon     = float(lon)
        alt     = float(alt)
        hAcc    = float(hAcc)
        vAcc    = float(vAcc)
        speed   = float(speed)
        dformat = "%Y-%m-%d %H:%M:%S"
        dt      = datetime.datetime.strptime(dt, dformat)
        
        if trip_id not in self.trips_by_id.keys():
            t = Trip(trip_id)
            t.startDatetime = dt
            self.trips.append(t)
            self.trips_by_id[t.trip_id] = t
            self.pointNum = 1
        else:
            self.pointNum +=1
        
        trip = self.trips_by_id[trip_id]
        
        p = Point( self.pointNum, trip, lat, lon, alt, hAcc, vAcc, speed, dt)
        
        self.points.append(p)
        self.points_by_id[ (trip_id, self.pointNum) ] = p
        
        trip.points_by_id[ (trip_id, self.pointNum) ] = p
        trip.points.append(p)
        
    def readTrip(self, csvLine_trip):
        (trip_id,user_id, age, gender, homeZIP, schoolZIP, workZIP, cycling_freq, purpose) = csvLine_trip.strip().split(",")
        trip_id = int(trip_id)
        user_id = int(user_id)
        
        if user_id not in self.users_by_id.keys():
            u = User( user_id )
            
            if age:
                u.age          = int(age)
            else: 
                u.age          = 0
            if gender:
                u.gender       = gender[0].upper()
            else:
                u.gender       = None
            if homeZIP:
                u.homeZIP      = int(homeZIP)
            else:
                u.homeZIP      = 0
            if schoolZIP:
                u.schoolZIP    = int(schoolZIP)
            else:
                u.schoolZIP    = 0
            if workZIP:
                u.workZIP      = int(workZIP)
            else:
                u.workZIP      = 0
            if cycling_freq:
                u.cycling_freq = cycling_freq
            else:
                u.cycling_freq = None
        
            # add user to db
            self.users.append(u)
            self.users_by_id[u.user_id] = u
        
        if trip_id not in self.trips_by_id.keys():
            raise("trip not in database yet!")
        
        
        t = self.trips_by_id[trip_id]
        u = self.users_by_id[user_id]
        
        # add trip attributes
        t.user    = u
        t.user_id = user_id
        t.purpose = purpose
       
        # add trip to user
        u.trips.append(t)
        u.trips_by_id[trip_id] = t
        

    def printToFile(self, SEPARATE_CSV_LOC, SEPARATE_CSV_PREFIX, append = False):
        
        min_trip_id = str(min(self.trips_by_id.keys()))
        max_trip_id = str(max(self.trips_by_id.keys()))
        
        users_out = os.path.join(SEPARATE_CSV_LOC, SEPARATE_CSV_PREFIX + "_USERS" + min_trip_id+"-" + max_trip_id + ".csv")
        trips_out = os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_TRIPS" + min_trip_id+"-" + max_trip_id + ".csv")
        points_out= os.path.join(SEPARATE_CSV_LOC,SEPARATE_CSV_PREFIX+"_POINTS" + min_trip_id+"-" + max_trip_id + ".csv")
        
        if append:
            f_u = open(users_out,  mode="a")
            f_t = open(trips_out,  mode="a")
            f_p = open(points_out, mode="a")
        else:
            f_u = open(users_out,  mode="w")
            f_t = open(trips_out,  mode="w")
            f_p = open(points_out, mode="w")
            
            f_u.write(",".join(User.csv_outfile_fields) + "\n" )
            f_t.write(",".join(Trip.csv_outfile_fields) + "\n" )
            f_p.write(",".join(Point.csv_outfile_fields) + "\n")
            
        for u in self.users:
            f_u.write(u.csvLine())
        f_u.close()
        print "finished writing to %s" % (users_out)
        
        for t in self.trips:
            f_t.write(t.csvLine())
        f_t.close()
        print "finished writing to %s" % (trips_out)
        
        for p in self.points:
            f_p.write(p.csvLine())
        f_p.close()
        print "finished writing to %s" % (points_out)
        
        return (users_out, trips_out, points_out)

class User(object):
    
    csv_outfile_fields = ["user_id", "age", "gender", "homeZIP", "schoolZIP", "workZIP", "cycling_freq", "numTrips", "firstTrip", "lastTrip"]
    
    def __init__(self, user_id):
        #USER DEFINITION
        self.user_id     = user_id
        self.trips       = []
        self.trips_by_id = {}
        
        #USER ATTRIBUTES       
        self.age          = 0
        self.gender       = None
        self.homeZIP      = 0
        self.schoolZIP    = 0
        self.workZIP      = 0
        self.cycling_freq = None
        
        self.firstTrip    = None
        self.lastTrip     = None
        
        #TRIP ATTRIBUTES
        self.numTrips     = None
        
    def __repr__(self):
        #           userid      trips          age           gender       homeZIP      schoolZIP     workZIP       cyclingFreq
        return "%14s: %12d\n  %12s: %12d\n  %12s: %12d\n  %12s: %12s\n  %12s: %12d\n  %12s: %12d\n  %12s: %12d\n  %12s: %12s\n" % ("user_id", self.user_id, "trips", self.getNumTrips(), "age",self.age, "gender", self.gender, "homeZIP", self.homeZIP, "schoolZIP", self.schoolZIP, "workZIP", self.workZIP, "cycling_freq", self.cycling_freq)

    def updateAttributes(self):
        self.numTrips  = len(self.trips)
        self.firstTrip = str(self.trips[0].points[0].dt.date())
        self.lastTrip  = str(self.trips[-1].points[0].dt.date())
        
    def csvLine(self):
        self.updateAttributes()
        outstr = ''
        for field in User.csv_outfile_fields:
            outstr+="%s," % (str(self.__dict__[field]))
        outstr+="\n"
        return outstr

class Trip(object):
    def __init__(self, trip_id):
        #TRIP DEFINITION
        self.trip_id = trip_id
        self.purpose = None
        self.points_by_id = {}
        self.points       = []
        
        #TRIP ATTRIBUTES
        self.numPoints     = 0
        self.startDatetime = None
        self.endDatetime   = None
        self.startDate     = None
        self.endDate       = None
        self.startHour     = 0
        self.endHour       = 0
        self.maxSpeed      = 0

        #USER ATTRIBUTES
        self.user         = None
        self.user_id      = None
        self.cycling_freq = None
        self.age          = 0
        self.gender       = None
        self.homeZIP      = 0
        self.schoolZIP    = 0
        self.workZIP      = 0
        
    csv_outfile_fields = ["trip_id", "user_id", "purpose", "numPoints", "gender", "age", "cycling_freq", "startDate", "startHour"]
        
    def __repr__(self):
        return "%12s: %12d\n  %10s: %12d\n  %10s: %12s\n  %10s: %12d\n" % ("trip_id",self.trip_id, "user_id",self.user_id, "purpose", self.purpose, "points", self.getNumPoints())

    def updateAttributes(self):
        self.user_id      = self.user.user_id
        self.cycling_freq = self.user.cycling_freq
        self.age          = self.user.age
        self.gender       = self.user.gender
        self.homeZIP      = self.user.homeZIP
        self.schoolZIP    = self.user.schoolZIP
        self.workZIP      = self.user.workZIP
        
        self.numPoints     = len(self.points)
        self.startDatetime = self.points[0].dt
        self.endDatetime   = self.points[-1].dt
        self.startDate     = str(self.points[0].dt.date())
        self.endDate       = str(self.points[-1].dt.date())
        self.startHour     = self.startDatetime.hour
        self.endHour       = self.endDatetime.hour
        self.maxSpeed      = 0
        
    def csvLine(self):
        self.updateAttributes()
        outstr = ''
        for field in Trip.csv_outfile_fields:
            outstr+="%s," % (str(self.__dict__[field]))
        outstr+="\n"
        return outstr

class Point(object):
    def __init__(self, pointNum, trip, lat, lon, alt, hAcc, vAcc, speed, dt):
        #POINT DEFINITION
        self.pointNum  = pointNum
        self.latitude  = lat
        self.longitude = lon
        self.altitude  = alt
        self.hAccuracy = hAcc
        self.vAccuracy = vAcc
        self.speed     = speed
        self.dt        = dt
        self.date      = str(dt.date())
        self.hour      = dt.hour
        
        #POINT ATTRIBUTES
        self.isStart   = None
        self.isEnd     = None
        
        #TRIP ATTRIBUTES
        self.trip     = trip
        self.trip_id  = trip.trip_id
        self.purpose  = None
        
        #USER ATTRIBUTES
        self.user         = None
        self.user_id      = 0
        self.cycling_freq = 0
        
    csv_outfile_fields = ["pointNum", "trip_id", "purpose", "user_id", "cycling_freq", "latitude", "longitude", "altitude", "dt", "date", "hour", "hAccuracy", "vAccuracy"]
        
    def __repr__(self):
        return "%10s: %22d\n  %8s: %22d\n  %8s: %22s\n  %8s: %22.4f\n  %8s: %22.4f\n  %8s: %22.4f\n" % ("point_id", self.pointNum, "trip_id", self.trip_id, "datetime", str(self.dt), "lat", self.latitude, "lon", self.longitude, "altitude", self.altitude)

    def updateAttributes(self):
        self.purpose  = self.trip.purpose
        
        self.user         = self.trip.user
        self.user_id      = self.user.user_id
        self.cycling_freq = self.user.cycling_freq

    def csvLine(self):
        self.updateAttributes()
        outstr = ''
        for field in Point.csv_outfile_fields:
            outstr+="%s," % (str(self.__dict__[field]))
        outstr+="\n"
        return outstr
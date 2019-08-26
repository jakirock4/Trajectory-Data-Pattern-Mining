class RutasGPS:
    def __init__(self, id, deviceid, valid, latitude, longitude, devicetime, speed, attributes):
        self.id = id
        self.deviceid = deviceid
        self.valid = valid
        self.latitude = latitude
        self.longitude = longitude
        self.devicetime = devicetime
        self.speed = speed
        self.attributes = attributes

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class Location:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

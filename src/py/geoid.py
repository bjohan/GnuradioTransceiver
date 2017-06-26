class Geoid:
    def __init__(self):
        self.a = 6378137.0;
        self.b = self.a;
        self.c = 6356752.314245;

    def radius(self, lon, lat):
        #lon -pi to pi
        #lat -pi/2 to pi/2
        x = self.a*cos(lat)*cos(lon)
        y = self.b*cos(lat)*sin(lon)
        z = self.c*sin(lat)

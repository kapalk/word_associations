
import math
import os
import sys

class NotExists(Exception):
    pass

class DistanceEvaluator:

    NOT_EXISTS = -1

    def __init__(self):
        self.dir = os.path.dirname(__file__)
        self.coordinates = self._read_coordinates()

    def get_distances(self, reference, countries):
        return [self.get_distance(reference, country) for country in countries]

    def get_distance(self, country_a, country_b):

        try:
            coord_a = self._get_coordinates(country_a)
            coord_b = self._get_coordinates(country_b)
            
            lat1 = math.radians(coord_a[0])
            lon1 = math.radians(coord_a[1])
            lat2 = math.radians(coord_b[0])
            lon2 = math.radians(coord_b[1])
            
            R = 6371 # kilometers
            alpha = math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2 - lon1))
            return R*alpha
        
        except NotExists:
            return DistanceEvaluator.NOT_EXISTS

    def _read_coordinates(self):

        coordinates = {}
        with open(os.path.join(self.dir, 'coordinates.csv'), 'r') as fp:
            for idx, line in enumerate(fp):
                code, lat, lon, country = line.strip().split('\t')
                try:
                    coordinates[country] = (float(lat), float(lon))
                except Exception as e:
                    pass
        return coordinates

    
    def _get_coordinates(self, country):

        country = country.capitalize()
        #print(self.coordinates)
        if country not in self.coordinates.keys():
            raise NotExists()

        return self.coordinates[country]
    

if __name__ == '__main__':

    evaluator = DistanceEvaluator()
    ref = sys.argv[1]
    countries = sys.argv[2:]

    print(evaluator.get_distances(ref,countries))
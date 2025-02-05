
def read_coords(fp): 
    coords = []
    with open(fp) as f:
        for coord in f.readlines():
            if ',' in coord:
                lat, lon = coord.split(',')
                coords.append((float(lat), float(lon)))
    return coords

class DistanceMatrix:
    def __init__(self, fp):
        with open(fp) as f:
            distances = [[float(x) for x in line.split()] for line in f]
        self.distances = distances
    
    def size(self):
        return len(self.distances)

    def distance_to(self, frm, to):
        if frm > to:
            frm, to = to, frm
        return self.distances[frm][to]

    def distance_path(self, path):
        if not path:
            return 0
        return self.distance_to(0, path[0]) + self.distance_to(0, path[-1]) + \
            sum(self.distance_to(path[i], path[i + 1]) for i in range(len(path) - 1))

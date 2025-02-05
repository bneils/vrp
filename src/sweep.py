from geographiclib.geodesic import Geodesic

# Module to compute the VRP with the Sweep Algorithm.

def bearing(coord1, coord2):
    # CW from north.
    return Geodesic.WGS84.Inverse(coord1[0], coord1[1], coord2[0], coord2[1])['azi1']

def sort_points_by_bearing(coords):
    """ Orders coordinates by angle bearing around the first coordinate and excludes first coordinate.
    Do not make assumptions about which order is returned. """
    polar_coords = []
    for i, coord in enumerate(coords):
        if i == 0:
            continue
        angle = bearing(coords[0], coords[i])
        if angle < 0:
            angle += 360
        polar_coords.append((angle, i))
    polar_coords.sort(reverse=True)
    polar_coords = [c[1] for c in polar_coords]
    return polar_coords

def build_path_recursively(pool, validator, path=[]):
    """ Yields only valid paths. """
    # The caller has given us a path that _was_ valid but may've been invalidated
    # by the last location - so if it's invalid remove the last location.
    if not validator(path):
        return path[:-1]

    # Preceding the loop, we have verified the path is valid.
    for i in pool:
        # Attempt to add i to the path, which may invalidate or validate the path.
        new_path = path + [i]
        new_pool = pool.copy()
        new_pool.remove(i)
        yield from build_path_recursively(new_pool, validator, new_path)
    
    if not pool:
        yield path

def tsp(locs, validator, distances):
    """ Trivially computes Traveling Salesman solution by bruteforce. """
    paths = list(build_path_recursively(locs, validator))
    if not paths:
        return [], float('inf')
    path = min(paths, key=distances.distance_path)
    return path, distances.distance_path(path)

def sweep(coords, distances, max_miles, max_stops):
    """ Returns a tuple containing the solution distance and solution. """
    polar_coords = sort_points_by_bearing(coords)
    min_cost = float('inf')
    optimal_path = []
    k = max_stops
    M = max_miles
    n = len(coords)

    def validator(path):
        return len(path) <= k and distances.distance_path(path) <= M

    # Depending on which seed coordinate the algorithm starts at may
    # change what solution is returned, so N solutions are made to
    # find an optimal solution, which is Omega N^2 runtime.
    for r in range(len(polar_coords)):
        new_polar_coords = polar_coords[r:] + polar_coords[:r]

        # Continue adding points to a cluster iff:
        # - Doing so results in the roundtrip <= M
        # - No more than k stops.
        total_cost = 0
        paths = []
        cluster = []
        for i in new_polar_coords:
            # Sweep won't come up with an answer if some locations can't be made into a route
            if not validator([i]):
                paths.append([i])
                total_cost += distances.distance_path([i])
                continue
            cluster.append(i)
            path, cost = tsp(cluster, validator, distances)
            if len(cluster) > k or cost > M:
                # Then removing i results in the largest cluster.
                path, cost = tsp(cluster[:-1], validator, distances)
                total_cost += cost
                paths.append(path)

                # Next cluster starts out with i.
                cluster = [i]

        if total_cost < min_cost:
            min_cost = total_cost
            optimal_path = paths

    return (min_cost, optimal_path)
from pyvrp import Model
#from pyvrp.plotting import plot_coordinates, plot_solution
from pyvrp.stop import MaxRuntime
#import matplotlib.pyplot as plt

import helper

"""
Warning: pyvrp does not process floats!
This uses fixed prec decimals.
"""

def pyvrp(coords, distances, max_miles, max_stops):
    MAX_TIME = 1
    PRECISION = 100

    demands = [1] * len(coords)
    demands[0] = 0

    m = Model()
    m.add_vehicle_type(len(coords), capacity=max_stops, max_distance=int(max_miles * PRECISION))
    depot = m.add_depot(x=coords[0][0], y=coords[0][1])
    clients = [
        (idx, m.add_client(x=coords[idx][0], y=coords[idx][1], delivery=demands[idx]))
        for idx in range(1, len(coords))
        if distances.distance_path([idx]) <= max_miles
    ]

    invalid_paths = [(i,) for i, coord in enumerate(coords) if distances.distance_path([i]) > max_miles]
    locations = [(0, depot)] + clients
    for i, frm in locations:
        for j, to in locations:
            d = distances.distance_to(i, j) * PRECISION
            m.add_edge(frm, to, distance=d)

    res = m.solve(stop=MaxRuntime(MAX_TIME), display=False)
    cost = res.cost() / PRECISION
    invalids_cost = sum(distances.distance_path(p) for p in invalid_paths)
    return cost + invalids_cost, res.best.routes() + invalid_paths

    #_, ax = plt.subplots(figsize=(8, 8))
    #plot_solution(res.best, m.data(), ax=ax)
    #plt.show()
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
        m.add_client(x=coords[idx][0], y=coords[idx][1], delivery=demands[idx])
        for idx in range(1, len(coords))
    ]

    locations = [depot] + clients
    for i, frm in enumerate(locations):
        for j, to in enumerate(locations):
            d = distances.distance_to(i, j) * PRECISION
            m.add_edge(frm, to, distance=d)

    res = m.solve(stop=MaxRuntime(MAX_TIME), display=False)
    cost = res.cost() / PRECISION
    return cost, res.best.routes

    #_, ax = plt.subplots(figsize=(8, 8))
    #plot_solution(res.best, m.data(), ax=ax)
    #plt.show()
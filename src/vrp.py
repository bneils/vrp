import sys

import helper
from sweep import sweep
from clarke_wright import clarke_wright
from mod_pyvrp import pyvrp

if __name__ == '__main__':
    num_arguments = 4
    if len(sys.argv) < num_arguments + 1:
        sys.stderr.write('vrp.py: computes solution to VRP and writes solution to stdout\n')
        sys.stderr.write('argument usage: coord_path dist_path max_miles max_stops [-h names_path]\n')
        sys.exit(1)

    coords = helper.read_coords(sys.argv[1])
    distances = helper.DistanceMatrix(sys.argv[2])
    M = max_miles = float(sys.argv[3])
    k = max_stops = int(sys.argv[4])

    print_readable = len(sys.argv) >= 6 and sys.argv[5] == '-h'
    if print_readable:
        names_path = sys.argv[6]

        with open(names_path) as f:
            name_lines = f.read().split('\n')

    solutions = []

    for max_stops_new in range(max_stops, 0, -1):
        sys.stderr.write(f"Best solution for max_stops = {max_stops_new}\n")

        sol1 = sweep(coords, distances, max_miles, max_stops_new) + ("Sweep", max_stops_new)
        sol2 = clarke_wright(coords, distances, max_miles, max_stops_new) + ("Clarke-Wright", max_stops_new)
        sol3 = pyvrp(coords, distances, max_miles, max_stops_new) + ("PyVRP", max_stops_new)

        solutions.extend((sol1, sol2, sol3))

        sys.stderr.write(f"Clarke-Wright: {sol2[0]}\n")
        sys.stderr.write(f"Sweep: {sol1[0]}\n")
        sys.stderr.write(f"PyVRP: {sol3[0]}\n")
    
    min_cost, optimal_path, author, new_max_stops = min(solutions, key=lambda s: s[0])
    min_cost = round(min_cost, 2)

    if not print_readable:
        content = str(min_cost) + '\n' + '\n'.join(' '.join(map(str, p)) for p in optimal_path)
        sys.stdout.write(content)
    else:
        print("Cost:", min_cost)
        sys.stderr.write(f"Optimal algorithm: {author}\n")
        sys.stderr.write(f"Maximum stops: {new_max_stops}\n")
        for routeIndex, route in enumerate(optimal_path):
            for j, loc in enumerate(route):
                name = name_lines[loc]
                lat, lon = coords[loc]
                lat, lon = round(float(lat), 4), round(float(lon), 4)
                print(f"{routeIndex+1}.{j+1}: {lat},{lon} {name}")
            print()
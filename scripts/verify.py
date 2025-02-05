import sys
import helper

# For testing purposes, verifies the outputted file has the correct distance.

with open(sys.argv[1]) as f:
    solution = f.readlines()
    claimed_cost = float(solution[0])
    paths = [[int(x) for x in line.split()] for line in solution[1:]]

distances = helper.DistanceMatrix(sys.argv[2])

print("Actual:", sum(map(distances.distance_path, paths)))
print("Expected:", claimed_cost)

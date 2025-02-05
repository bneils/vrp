#!/usr/bin/python3
import requests
import json
import sys

HOST_IP = 'http://127.0.0.1:5000'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('usage: ./prepdata.py {coordinate_file}')
        exit(1)

    file_name = sys.argv[1]
    with open(file_name) as f:
        lines = f.read().split('\n')
    coords = []
    for line in lines:
        if ',' not in line:
            continue
        lat, lon = line.split(',')
        coords.append((float(lat), float(lon)))

    # Each row is i
    # Each column is j
    # [i,j] is the distance between i and j.
    # i < j.
    lines = []

    # Let the first coordinate be the depot.
    depot = coords[0]
    for i in range(len(coords)):
        row = [0] * (i + 1)
        for j in range(i + 1, len(coords)):
            coord0 = coords[i]
            coord1 = coords[j]
            request_str = f'{HOST_IP}/route/v1/driving/{coord0[1]},{coord0[0]};{coord1[1]},{coord1[0]}?steps=true&alternatives=3&exclude=toll'
            resp = requests.get(request_str)
            obj = json.loads(resp.content)
            shortest_route = min(obj['routes'], key=lambda r: r['distance'])
            miles = round(0.6214 / 1000 * shortest_route['distance'], 4)
            row.append(miles)
        lines.append(' '.join(map(str, row)))

    content = '\n'.join(lines)

    with open('distance_matrix.txt', 'w') as f:
        f.write(content)

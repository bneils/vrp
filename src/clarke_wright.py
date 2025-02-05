
# Module to compute the VRP with the Clarke Wright algorithm.
# Based on my C++ implementation which I found too cumbersome.

def calculate_savings_matrix(distances):
    n = distances.size()
    mat = [[0] * n for _ in range(n)]
    for i in range(1, n):
        for j in range(i + 1, n):
            savings = distances.distance_to(0, i) + \
                distances.distance_to(0, j) - \
                distances.distance_to(i, j)

            mat[i][j] = savings
    return mat

class Routes:
    def __init__(self, n):
        self.route_refs = [None] * n
        self.n = n
    
    def is_assigned(self, i):
        return self.route_refs[i] != None
    
    def create_simple_route(self, i, j, validator):
        p = [i, j]
        if not validator(p):
            return
        # Assign reference to p to each index.        
        self.route_refs[i] = self.route_refs[j] = p
        return p

    def is_not_interior(self, i):
        if not self.is_assigned(i):
            return False
        return self.route_refs[i][0] == i or self.route_refs[i][-1] == i

    def route_append(self, i, j, validator):
        p = self.route_refs[i]
        p_copy = p.copy()

        def insert(p):         
            if p[0] == i:
                p.insert(0, j)
            elif p[-1] == i:
                p.append(j)

        # Preview the change, do not commit it if
        # it results in a bad path.
        insert(p_copy)

        if not validator(p_copy):
            return
        
        insert(p)
        self.route_refs[j] = p
        return p
    
    def route_merge(self, i, j, validator):
        r1, r2 = self.route_refs[i], self.route_refs[j]
        i_pos = 0 if r1[0] == i else -1
        j_pos = 0 if r2[0] == j else -1

        if i_pos == j_pos:
            r_new = r1[::-1] + r2 if i_pos == 0 else r1 + r2[::-1]
        elif i_pos == 0:
            r_new = r2 + r1
        else:
            r_new = r1 + r2
        
        if not validator(r_new):
            return
        
        for n in r_new:
            self.route_refs[n] = r_new
        
        return r_new
    
    def current_routes(self, distances):
        visited = [False] * self.n
        routes = []
        for i in range(1, self.n):
            if visited[i]:
                continue
            route = self.route_refs[i]
            if route is None:
                routes.append([i])
            else:
                for n in route:
                    visited[n] = True
                routes.append(route)
        cost = sum(distances.distance_path(r) for r in routes)
        return (cost, routes)

def clarke_wright(coords, distances, max_miles, max_stops):
    savings_mat = calculate_savings_matrix(distances)
    n = distances.size()
    savings = [((i, j), savings_mat[i][j]) for i in range(1, n) for j in range(i + 1, n)]
    savings.sort(key=lambda s: s[1], reverse=True)

    def validator(path):
        return len(path) <= max_stops and distances.distance_path(path) <= max_miles

    routes = Routes(n)
    for (i, j), _ in savings:
        # Add edge to a route.
        i_assigned = routes.is_assigned(i)
        j_assigned = routes.is_assigned(j)
        i_not_interior = routes.is_not_interior(i)
        j_not_interior = routes.is_not_interior(j)

        if not i_assigned and not j_assigned:
            routes.create_simple_route(i, j, validator)
        elif i_assigned != j_assigned:
            if i_assigned:
                if not i_not_interior:
                    continue
                routes.route_append(i, j, validator)
            else:
                if not j_not_interior:
                    continue
                routes.route_append(j, i, validator)
        else: # i_assigned and j_assigned
            if not i_not_interior and not j_not_interior:
                continue
            routes.route_merge(i, j, validator)

    return routes.current_routes(distances)
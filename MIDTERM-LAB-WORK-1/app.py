import heapq

edges = [
    (1, 2, 10, 15, 1.2),
    (1, 6, 10, 15, 1.2),
    (2, 3, 12, 25, 1.5),
    (2, 5, 12, 25, 1.5),
    (2, 6, 10, 15, 1.2),
    (3, 4, 12, 25, 1.5),
    (3, 5, 12, 25, 1.3),
    (4, 5, 14, 25, 1.2),
    (5, 6, 10, 25, 1.5),
    (6, 3, 10, 25, 1.3)
]

def build_graph(cost_index):
    graph = {i: {} for i in range(1, 7)}
    for u, v, d, t, f in edges:
        costs = [d, t, f]
        weight = costs[cost_index]
        graph[u][v] = weight
        graph[v][u] = weight
    return graph

def dijkstra_with_paths(graph, start):
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    paths = {}
    for node in graph:
        if node == start:
            continue
        path = []
        curr = node
        while curr is not None:
            path.append(curr)
            curr = previous_nodes[curr]
        path.reverse()
        paths[node] = (path, distances[node])
        
    return sum(distances.values()), paths

metrics = ["Distance", "Time", "Fuel"]
for i, metric in enumerate(metrics):
    graph = build_graph(i)
    best_node = None
    min_total = float('inf')
    best_paths = {}
    
    for node in range(1, 7):
        total_cost, paths = dijkstra_with_paths(graph, node)
        if total_cost < min_total:
            min_total = total_cost
            best_node = node
            best_paths = paths
            
    print(f"--- Minimal {metric} Cost is from Node {best_node} (Total: {min_total:.1f}) ---")
    for dest, (path, cost) in best_paths.items():
        path_str = " -> ".join(map(str, path))
        print(f"To Node {dest}: {path_str} (Cost: {cost:.1f})")
    print()
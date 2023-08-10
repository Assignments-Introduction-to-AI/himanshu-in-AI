from expand import expand

def a_star_search(dis_map, time_map, start, end, heuristic):
    open_list = [(start, 0)]
    came_from = {}
    g_score = {node: float('inf') for node in dis_map}
    g_score[start] = 0
    f_score = {node: float('inf') for node in dis_map}
    f_score[start] = heuristic(dis_map[start][end], time_map[start][end])

    while open_list:
        current, _ = min(open_list, key=lambda x: f_score[x[0]])
        open_list.remove((current, f_score[current]))
        expand.expand_count += 1

        if current == end:
            path = reconstruct_path(came_from, current)
            return path

        neighbors = expand(current, time_map)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + dis_map[current][neighbor]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(dis_map[neighbor][end], time_map[neighbor][end])
                if neighbor not in [x[0] for x in open_list]:
                    open_list.append((neighbor, f_score[neighbor]))

    return None 

def depth_first_search(time_map, current, goal, visited=None):
    if visited is None:
        visited = set()
    if current == goal:
        return [current]
    if current in visited:
        return None

    visited.add(current)
    neighbors = expand(current, time_map)
    for neighbor in neighbors:
        path = depth_first_search(time_map, neighbor, goal, visited.copy())
        if path:
            return [current] + path
    return None

def breadth_first_search(time_map, start, goal):
    queue = [(start, [start])]

    while queue:
        (vertex, path) = queue.pop(0)
        neighbors = expand(vertex, time_map)
        for next_vertex in neighbors:
            if next_vertex in path:
                continue
            if next_vertex == goal:
                return path + [next_vertex]
            else:
                queue.append((next_vertex, path + [next_vertex]))

    return None 

def heuristic(distance, time):
    return distance + time

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path

if __name__ == "__main__":
    start_landmark = 'Campus'
    goal_landmark = 'Ryan_Field'
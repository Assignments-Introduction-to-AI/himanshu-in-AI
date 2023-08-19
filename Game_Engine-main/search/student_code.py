from expand import expand

import heapq

def a_star_search(dis_map, time_map, start, end):
    def heuristic(node):
        return dis_map[node][end]  # Using distance as heuristic

    open_list = [(0, start)]
    came_from = {}
    g_score = {node: float('inf') for node in dis_map}
    g_score[start] = 0
    f_score = {node: float('inf') for node in dis_map}
    f_score[start] = heuristic(start)

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node == end:
            path = [current_node]
            while current_node in came_from:
                current_node = came_from[current_node]
                path.append(current_node)
            path.reverse()
            return path

        x = expand(current_node, dis_map)
        for neighbor in x:
            if time_map[current_node][neighbor] is not None:
                tentative_g_score = g_score[current_node] + time_map[current_node][neighbor]
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path found


def depth_first_search(time_map, start, end):
    
    queue = [start]  # Queue contains tuples of (current landmark, path)
    parents = {}
    found = False

    while queue:
        current = queue.pop(0)
        
        if current == end:
            found = True
            break
        
        nodes = expand(current, time_map)
        for childnodes in nodes:
            queue.insert(0,childnodes)
            parents[childnodes]=current
    path = [end]
    if found == True:
        current = end
        while current!=start:
            path.insert(0,parents[current])
            current = parents[current]
    return path  # No path found



def breadth_first_search(time_map, start, end):
    
    
    queue = [start]  # Queue contains tuples of (current landmark, path)
    visited = []
    parents = {}
    found = False

    while queue:
        current = queue.pop(0)
        
        if current == end:
            found = True
            break
        
        if current not in visited:
            visited.append(current)
            nodes = expand(current, time_map)
            for childnodes in nodes:
                if childnodes not in visited:
                    queue.append(childnodes)
                    parents[childnodes]=current
    path = [end]
    if found == True:
        current = end
        while current!=start:
            path.insert(0,parents[current])
            current = parents[current]
    return path  # No path found


print(a_star_search)


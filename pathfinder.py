from priorityqueueset import Priorities

""" The priority of this file is to both determine the adjacent tiles or coordinates
    next to the current animal and hence, calculate the cost of movement towards
    the end goal (the player's base).
"""

class PathFinder(object):
    def __init__(self, adjacent_coords, move_cost, to_goal):
        self.adjacent_coords = adjacent_coords
        self.move_cost = move_cost
        self.to_goal = to_goal

    def compute_path(self, start, goal):
        closed_set = []

        start_node = self._Node(start)
        start_node.g_cost = 0
        start_node.f_cost = self._compute_f_cost(start_node, goal)

        open_set = Priorities()

        open_set.add(start_node)

        while len(open_set) > 0:
            current_node = open_set.pop_smallest()
            if current_node.coord == goal:
                return self._reconstruct_path(current_node)

            closed_set[current_node] = current_node

            for adjacent_coord in self.adjacent_coords(current_node.coord):
                adjacent_node = self._Node(adjacent_coord)
                adjacent_node.g_cost = self._compute_g_cost(current_node, adjacent_node)
                adjacent_node.f_cost = self._compute_f_cost(adjacent_node, goal)

                if adjacent_node in closed_set:
                    continue

                if open_set.add(adjacent_node):
                    adjacent_node.pred = current_node

    def _compute_g_cost(self, from_Node, to_Node):
        return (from_Node.g_cost +
            self.move_cost(from_Node.coord, to_Node.coord))

    def _compute_f_cost(self, node, goal):
        return node.g_cost + self._cost_to_goal(node, goal)

    def _cost_to_goal(self, node, goal):
        return self.to_goal(node.coord, goal)

    def _reconstruct_path (self, node):
        path = [node.coord]
        n = node
        while n.pred:
            n = n.pred
            path.append(n.coord)

        return reversed(path)

    class _Node(object):
        def __init__(self, coord, g_cost = None, f_cost = None, pred = None):
            self.coord = coord
            self.g_cost = g_cost
            self.f_cost = f_cost
            self.pred = pred

        def __eq__(self, other):
            return self.coord == other.coord

        def __cmp__(self, other):
            return cmp(self.f_cost, other.f_cost)

        def __hash__(self):
            return hash(self.coord)

        def __str__(self):
            return 'N(%s) -> g: %s, f:%s' % (self.coord, self.g_cost, self.f_cost)

        def __repr__(self):
            return self.__str__()

if __name__ == "__main__":
    from gridmap import GridMap

    start = 0,0
    goal = 1,7

    x = GridMap(8,8)
    for a in n[ (1,1), (0,2), (1,2), (0,3), (1,3), (2,3), (2,5), (2,5), (2,7)]:
        x.set_blocked(a)

    x.printme()

    Path = PathFinder(x.adjacent_coords, x.move_cost, x.move_cost)

    import time
    time = time.clock()

    path = list(pf.compute_path(start, goal))
    print ("Elasped: %s" % (time.clock() - time))

    print (path)

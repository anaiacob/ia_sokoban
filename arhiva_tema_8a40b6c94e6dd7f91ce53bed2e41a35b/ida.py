import time
from search_methods.heuristics import manhattan_with_deadlock_heuristic

class IDAStarSolver:
    def __init__(self, initial_map, heuristic=manhattan_with_deadlock_heuristic):
        self.initial_map = initial_map
        self.heuristic = heuristic
        self.nodes_expanded = 0

    def search(self):
        start_time = time.time()
        threshold = self.heuristic(self.initial_map)
        print(f"Threshold initial: {threshold}")

        while True:
            visited = set()
            path = []
            temp = self._search(self.initial_map, 0, threshold, visited, path)

            if isinstance(temp, list):
                end_time = time.time()
                print(f"Solutie gasita in {end_time - start_time:.2f} secunde, {self.nodes_expanded} noduri expandate.")
                return temp

            if temp == float('inf'):
                print("Nu s-a gasit solutie.")
                return None

            threshold = temp

    def _search(self, current_map, g, threshold, visited, path):
        f = g + self.heuristic(current_map)
        if f > threshold:
            return f

        if current_map.is_solved():
            return path

        min_threshold = float('inf')

        for neighbour in current_map.get_neighbours():
            state_id = str(neighbour)

            if state_id in visited:
                continue

            visited.add(state_id)
            self.nodes_expanded += 1

            result = self._search(neighbour, g + 1, threshold, visited, path + [neighbour])

            if isinstance(result, list):
                return result

            if result < min_threshold:
                min_threshold = result

            visited.remove(state_id)

        return min_threshold

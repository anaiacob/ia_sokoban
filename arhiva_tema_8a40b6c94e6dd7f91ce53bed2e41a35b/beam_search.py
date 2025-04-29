from sokoban.map import Map
from search_methods.heuristics import manhattan_with_deadlock_heuristic


class BeamSearch:
    def __init__(self, initial_map, beam_width=5):
        self.initial_map = initial_map
        self.beam_width = beam_width
        self.nodes_expanded = 0

    def search(self):
        # Initializare: fiecare element din frontiera e (harta_curenta, drum_pana_acum)
        frontier = [(self.initial_map, [])]

        while frontier:
            # Verificam daca vreo stare e deja solutie
            for state, path in frontier:
                if state.is_solved():
                    return path  # Gasit solutia!

            # Extindem toate nodurile
            new_frontier = []

            for state, path in frontier:
                for move, next_state in state.get_neighbours():
                    self.nodes_expanded += 1
                    new_path = path + [move]
                    new_frontier.append((next_state, new_path))

            # Sortam dupa euristica avansata: manhattan_with_deadlock_heuristic
            new_frontier.sort(key=lambda item: manhattan_with_deadlock_heuristic(item[0]))

            # Pastram doar cei mai buni beam_width copii
            frontier = new_frontier[:self.beam_width]

        # Daca s-a terminat fara solutie
        return None

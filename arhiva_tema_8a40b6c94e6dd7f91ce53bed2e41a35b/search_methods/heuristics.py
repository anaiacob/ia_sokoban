from sokoban import Box

# Verifica daca o pozitie (y, x) este valida in grid
def is_valid(current_map, y, x):
    return 0 <= y < len(current_map.map) and 0 <= x < len(current_map.map[0])

# Verifica daca la (y, x) este un perete ('W')
def is_wall(current_map, y, x):
    return is_valid(current_map, y, x) and current_map.map[y][x] == 'W'

# Extrage toate pozitiile cutiilor (Box) din harta
def get_boxes_positions(current_map):
    boxes_positions = []
    for y in range(len(current_map.map)):
        for x in range(len(current_map.map[0])):
            if isinstance(current_map.map[y][x], Box):
                boxes_positions.append((y, x))
    return boxes_positions

# Distanaa Manhattan masoara pentru fiecare cutie cat de 
# departe este de cea mai apropiata tinta (target), adunand diferentele de pe axe
#Deadlock detection (detectare de blocaj):
# Verificam daca o cutie a fost impinsa intr-un colt sau intr-o zona unde nu mai poate ajunge la nicio tinta (ex: intre doi pereti).
# Daca o cutie e blocata, consideram starea foarte proasta (de exemplu, returnam un cost urias float('inf')) pentru a evita acea miscare.
#https://ro.wikipedia.org/wiki/Distan%C8%9B%C4%83_Manhattan
def manhattan_with_deadlock_heuristic(current_map):
    total_distance = 0

    boxes = get_boxes_positions(current_map)
    goals = current_map.targets

    if not boxes or not goals:
        return float('inf')  # Fara cutii sau tinte => imposibil

    for (y, x) in boxes:
        # Verificare colturi (pereti adiacenti)
        adjacent_walls = 0
        if is_wall(current_map, y + 1, x):
            adjacent_walls += 1
        if is_wall(current_map, y - 1, x):
            adjacent_walls += 1
        if is_wall(current_map, y, x + 1):
            adjacent_walls += 1
        if is_wall(current_map, y, x - 1):
            adjacent_walls += 1

        if adjacent_walls >= 2 and (y, x) not in goals:
            return float('inf')  # Deadlock intr-un colt

        # Calculam distantele fata de tinte
        distances = []
        for goal in goals:
            distance = abs(x - goal[1]) + abs(y - goal[0])
            distances.append(distance)

        if not distances:
            return float('inf')  # Nicio tinta accesibila

        total_distance += min(distances)

        # Verificam blocaje intre cutii
        neighbours = [
            (y + 1, x),
            (y - 1, x),
            (y, x + 1),
            (y, x - 1)
        ]

        box_neighbours = [pos for pos in neighbours if pos in boxes]
        if len(box_neighbours) >= 2 and (y, x) not in goals:
            return float('inf')  # Blocaj de cutii

    return total_distance

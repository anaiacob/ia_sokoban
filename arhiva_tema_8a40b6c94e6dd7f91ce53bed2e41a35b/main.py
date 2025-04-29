from pathlib import Path
import yaml
import os

from sokoban import Map
from ida import IDAStarSolver
from sokoban.gif import create_gif
from utils.functions import complet_list_of_wrong_zone

# Setam directoare
folder_test_path = Path('tests')
gif_folder = Path('GIFS')
frames_folder = Path('frames_temp')

# Asiguram ca directoarele exista
os.makedirs(gif_folder, exist_ok=True)
os.makedirs(frames_folder, exist_ok=True)

# Citim fisierele YAML
yaml_files = sorted(folder_test_path.glob('*.yaml'))
yaml_data = [yaml.unsafe_load(open(f, 'r', encoding='utf-8')) for f in yaml_files]

# Main
if __name__ == '__main__':
    if not folder_test_path.exists():
        print(f"Folderul {folder_test_path} NU exista!")
    else:
        for idx, item in enumerate(yaml_data):
            yaml_file = yaml_files[idx]
            print("=" * 50)
            print(f"Testez harta: {yaml_file.name}")
            print("=" * 50)

            # Initializam harta
            map_from_yaml = Map.from_yaml(str(yaml_file))

            # Alegeti aici solverul: IDAStar sau BeamSearch
            solver = IDAStarSolver(map_from_yaml)
            # solver = BeamSearch(map_from_yaml, beam_width=10)

            solution = solver.search()

            if solution:
                print(f"Solutie gasita cu {len(solution)} mutari.")
                frames_folder_map = frames_folder / yaml_file.stem
                frames_folder_map.mkdir(parents=True, exist_ok=True)

                crt_map = Map.from_str(str(map_from_yaml))  # Corect
                idx_frame = 0
                crt_map.save_map(
                    save_path=frames_folder_map.as_posix(),
                    save_name=f"{idx_frame:03d}"
                )

                idx_frame += 1

                for move in solution:
                    crt_map.save_map(
                        save_path=frames_folder_map.as_posix(),
                        save_name=f"{idx_frame:03d}"
                    )

                    idx_frame += 1

                images_paths = sorted(frames_folder_map.glob('*.png'))
                images_paths = [str(img_path) for img_path in images_paths]

                gif_path = gif_folder / f"{yaml_file.stem}_solution.gif"
                create_gif(path_images=images_paths, gif_name=gif_path.name, save_path=str(gif_folder))

                print(f"GIF salvat la: {gif_path}")

            else:
                print("Nu s-a gasit nicio solutie.")

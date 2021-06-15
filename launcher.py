import os
import main
import random
import dill


def generate_world(name, size):
    level = []
    scale = main.Game.get_scale()
    for i in range(size):
        for j in range(size):
            level.append(main.Tile((i*scale, j*scale), "tiles:grass"))

    # ok now just do the thing where you start spots and grow them
    for i in range(random.randint(5, 10)):
        # ok I am kind of bored will write this later
        pass

    os.mkdir(f"data/levels/{name}")
    with open(f"data/levels{name}/level.pickle", "wb") as level_file:
        dill.dump(level, level_file)

    with open(f"data/levels{name}/entities.pickle", "wb") as entity_file:
        dill.dump([], entity_file)

    with open(f"data/levels{name}/inactive_entities.pickle", "wb") as inactive_entities_file:
        dill.dump([], inactive_entities_file)

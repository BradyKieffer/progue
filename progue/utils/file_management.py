""" Load a world """
import os
import dill

from progue.debug.logger import log_message

##########################################################################
# Helpers
##########################################################################
SAVES = 'saves/'
CHUNKS = 'chunks/'
WORLD_FILE_NAME = 'world.p'
ACTORS_FILE_NAME = 'actors.p'
PLAYER_FILE_NAME = 'player.p'


def create_if_not_exists(path):
    if not os.path.exists(path):
        # make the path
        os.makedirs(path)

##########################################################################
# Loading funcs
##########################################################################


def load_game(world_name, save_dir):
    saves_path = os.path.join(save_dir, SAVES + world_name)
    return {
        'World':  load(path=saves_path, file_name=WORLD_FILE_NAME),
        'Actors': load(path=saves_path, file_name=ACTORS_FILE_NAME)
    }


def load_chunk(save_dir, world_name, x, y):
    path = os.path.join(save_dir, SAVES + world_name, CHUNKS)
    chunk = load(path=path, file_name='chunk{x}{y}.p'.format(x=x, y=y))

    # log_message('Loaded {}'.format(chunk))
    return chunk


def load(path, file_name):
    """ Will return None if the file could not be found """
    load_path = os.path.join(path, file_name)
    if os.path.exists(load_path):
        return dill.load(open(load_path, 'rb'))
    return None

##########################################################################
# Saving funcs
##########################################################################


def save_game(game_engine, save_dir):
    """ Overall save func """
    create_if_not_exists(os.path.join(save_dir, SAVES))
    saves_path = os.path.join(
        save_dir,
        SAVES + game_engine.world.name
    )
    create_if_not_exists(saves_path)

    save(obj=game_engine.world,        path=saves_path, file_name=WORLD_FILE_NAME)
    save(obj=game_engine.world.actors,
         path=saves_path, file_name=ACTORS_FILE_NAME)
    save_chunks(world=game_engine.world, save_dir=save_dir)


def save_chunks(world, save_dir):
    base_path = os.path.join(save_dir, SAVES + world.name, CHUNKS)
    create_if_not_exists(base_path)
    for chunks in world.map:
        for chunk in chunks:
            save(obj=chunk, path=base_path, file_name=chunk.name + '.p')


def save_chunk(chunk, world_name, save_dir):
    base_path = os.path.join(save_dir, SAVES + world_name, CHUNKS)
    create_if_not_exists(base_path)
    save(obj=chunk, path=base_path, file_name=chunk.name + '.p')


def save(obj, path, file_name):
    save_dir = os.path.join(path, file_name)
    dill.dump(obj, open(save_dir, 'wb'))

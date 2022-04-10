from os import walk, listdir
import pickle

def get_pickles(sours_pickled_dump_path):
    for file in listdir(sours_pickled_dump_path):
        if '.pickle' not in file:
            continue
        with open(f'{sours_pickled_dump_path}/{file}', 'rb') as f:
            doc = pickle.load(f)
            yield file, doc

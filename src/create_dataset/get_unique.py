import json
import pretty_midi
import pypianoroll
import hdf5_getters
from tqdm import tqdm
import os
import concurrent.futures
import collections
import utils
from glob import glob
import pandas as pd

write = True
redo = False
output_dir = "../data_files/features/pianoroll"

def run_parallel(func, my_iter):
    # Parallel processing visualized with tqdm
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(func, my_iter), total=len(my_iter)))
    return results

def run():
    ### 6- Filter unique midis
    """LMD was created by creating hashes for the entire files
    and then keeping files with unique hashes.
    However, some files' musical content are the same, and only their metadata are different.
    So we hash the content (pianoroll array), and further filter out the unique ones."""
    # Create hashes for midis

    output_path = os.path.join(output_dir, "hashes.json")

    if os.path.exists(output_path) and not redo:
        with open(output_path, "r") as f:
            midi_file_to_hash = json.load(f)
    else:
        def get_hash_and_file(path):
            hash_ = utils.get_hash(path)
            file_ = os.path.basename(path)
            file_ = file_[:-4]
            return [file_, hash_]

        file_paths = sorted(glob(midi_dataset_path + "/**/*" + extension, recursive=True))

        print("Getting hashes for midis.")
        if __name__ == "__main__":
            midi_file_to_hash = run_parallel(get_hash_and_file, file_paths)
            midi_file_to_hash = sorted(midi_file_to_hash, key=lambda x:x[0])
            midi_file_to_hash = dict(midi_file_to_hash)
            if write:
                with open(output_path, "w") as f:
                    json.dump(midi_file_to_hash, f, indent=4)
                    print(f"Output saved to {output_path}")

    # also do the reverse hash -> midi
    output_path = os.path.join(output_dir, "unique_files.json")
    if os.path.exists(output_path) and not redo:
        with open(output_path, "r") as f:
            midi_files_unique = json.load(f)
    else:
        hash_to_midi_file = {}
        for midi_file, hash in midi_file_to_hash.items():
            try:
                best_match_score = best_match_scores_reversed[midi_file][1]
            except:
                best_match_score = 0
            if hash in hash_to_midi_file.keys():
                hash_to_midi_file[hash].append((midi_file, best_match_score))
            else:
                hash_to_midi_file[hash] = [(midi_file, best_match_score)]

        midi_files_unique = []
        # Get unique midis (with highest match score)
        for hash, midi_files_and_match_scores in hash_to_midi_file.items():
            if hash != "empty_pianoroll":
                midi_files_and_match_scores = sorted(midi_files_and_match_scores, key=lambda x: x[1], reverse=True)
                midi_files_unique.append(midi_files_and_match_scores[0][0])
        if write:
            with open(output_path, "w") as f:
                json.dump(midi_files_unique, f, indent=4)

    # create unique matched midis list
    midi_files_matched = list(match_scores_reversed.keys())

    output_path = os.path.join(output_dir, "midis_matched_unique.json")
    if os.path.exists(output_path) and not redo:
        with open(output_path, "r") as f:
            midi_files_matched_unique = json.load(f)
    else:
        midi_files_matched_unique = sorted(list(set(midi_files_matched).intersection(midi_files_unique)))
        if write:
            with open(output_path, "w") as f:
                json.dump(midi_files_matched_unique, f, indent=4)

    # create unique unmatched midis list
    output_path = os.path.join(output_dir, "midis_unmatched_unique.json")
    if os.path.exists(output_path) and not redo:
        with open(output_path, "r") as f:
            midi_files_unmatched_unique = json.load(f)
    else:
        midi_files_unmatched_unique = sorted(list(set(midi_files_unique) - set(midi_files_matched_unique)))
        if write:
            with open(output_path, "w") as f:
                json.dump(midi_files_unmatched_unique, f, indent=4)

if __name__ == "main":
    run()
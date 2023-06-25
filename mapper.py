"""#!/Users/ahmedbaruwa/opt/anaconda3/envs/thesis/bin/python
# -*- coding: latin-1 -*-
This script maps a CAESAR point cloud file to it's ground_truth labels
Useful when a pc_file has been transformed into canonical forms like SMPL
and only filename of PCs are available.
eg. CSR001a --> {lndmark_name : coords}
"""

import os
from pathlib import Path
import pickle
import sys

FNAMES_2_PATHS = "/projects/datascience/shared/DATA/raw_data/file_locs.pk" #sys.argv[1] #"/projects/datascience/shared/DATA/raw_data/file_locs.pk"
LND_NAMES_FILE = "/home/abaruwa/MS_Project/LASSO/landmark_names.txt" #sys.argv[2] #"/home/abaruwa/MS_Project/LASSO/landmark_names.txt"

class Mapper():
    def __init__(self, FNAMES_2_PATHS, LND_NAMES_FILE):
        """
        data_dir- path leading to all serialized pc_files in CAESAR
        pcs, and their labels.
        """
        self.fnames2paths = FNAMES_2_PATHS
        self.lndNamesFile = LND_NAMES_FILE
        self.data_dir = os.path.dirname(self.fnames2paths)
        self.fnames2paths = pickle.load(open(self.fnames2paths, 'rb')) # {file_keys : full_path to pickle files}

    def get_labels(self, pc_fname):
        """
        Input: 
            pc_fname - File name of a pc file e.g CSR001a
        Output: 
            A tuple (dict of groundtruth labels, full_path to pc_file)
        """
        file_key = Path(pc_fname).stem # remove file extension
        if file_key not in self.fnames2paths.keys(): 
            raise ValueError(f"pc fname - {pc_fname} not in data dir - {self.data_dir}")
        else:
            pc_data = pickle.load(open(self.fnames2paths[file_key], 'rb'))
        pc_labels = []
        # landmark names
        lnd_names = [line.rstrip() for line in open(self.lndNamesFile, 'r').readlines()]

        assert len(lnd_names)==74, f"length of landmark names must be 74 not {len(lnd_names)}"
        for name in sorted(lnd_names):
            pc_labels.append(pc_data[file_key]['LM'].get(name, (-999, -999, -999)))
        return pc_labels, self.fnames2paths[file_key]


def main():
    file_locs = sys.argv[1]
    LND_NAMES_FILE = sys.argv[2]
    file_key = sys.argv[3]
    m = Mapper(file_locs, LND_NAMES_FILE)
    _, full_path = m.get_labels(file_key)
    print(full_path)
    return


"""
TEST::: 
if __name__ == "__main__":
    mapper = Mapper(sys.argv[1], sys.argv[2])
    label_dict, pc_fpath = mapper.get_labels("csr132334a.npy")
    print (f"The ground truth landmarks of the file csr1534a is \n{label_dict}
    and the full path to the file is {pc_fpath}")
    
    python mapper.py "/projects/datascience/shared/DATA/raw_data/file_locs.pk" \
                    "/home/abaruwa/datascience/landmark_mine/scripts/landmark_names.txt"
                    "csr0001a"
"""
if __name__=="__main__":
    main()

# -*- coding: utf-8 -*-
#!/Users/ahmedbaruwa/opt/anaconda3/envs/thesis/bin/python

"""This file checks if a caaesr file has an input landmark or not
Input - filename, csr_lndname eg. return True or False or Error

Usage : python has_lnd.py "csr001a.pk" "10th rib midspine" "caesar" """

# from mapper import Mapper
# from pathlib import Path
import numpy as np
import pickle
import sys

class Tester():
    def __init__(self, landmark_name, data_type):
        self.landmark_name = landmark_name
        self.data_type = data_type

    def test(self ,fname):
        if self.data_type == "caesar":
            p = pickle.load(open(fname, 'rb'))
            key =list(p.keys())[0]
            lm_labels = list(p[key]['LM'])
            
        elif self.data_type == "shrec": #incomplete
            p = np.load(fname)

        FLAG = self.landmark_name in lm_labels
        #print(f"output of flag - {FLAG}")
        return FLAG

def main():
    fname = sys.argv[1]
    lnd_name = sys.argv[2]
    data_type = sys.argv[3] 
    
    
    tester = Tester(lnd_name, data_type)
    output=tester.test(fname)
    print(output)

if __name__=="__main__":
    main()
    

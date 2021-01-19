
#!/usr/bin/python

import numpy as np
import pandas as pd

def analyze_learning_dat(file_list):
    subject_data = {}
    for fl in file_list:

        #import data for each participant
                
        dat = pd.read_table(fl, 
                           delimiter= '\s+', 
                           header=None,
                           engine='python')

    # set accuracy to just 1 and 0 (2=incorrect,3=missed trial)
   
        # Double quotes need to be removed for string arrays
        if type(dat.loc[1,2]) == str:
            dat[2]=dat[2].str.replace('"','')
        # and re-formatted as numeric
            dat[2]=pd.to_numeric(dat[2])
        # Finally set accuracy
        dat.loc[dat[2]!=1 , 2] = 0
       
    # perform accuracy analysis
        # Find the different conditions and stimuli for the learning phase 
        findCond = {    
        "n3" : dat[0].str.contains("n3"),
        "m3" : dat[0].str.contains("m3"),
        "n6" : dat[0].str.contains("n6"),
        "m6" : dat[0].str.contains("m6")
        }
        findStim = {
        "stiA" : dat[1].str.contains("A"),
        "stiB" : dat[1].str.contains("B"),
        "stiC" : dat[1].str.contains("C"),
        "stiD" : dat[1].str.contains("D"),
        "stiE" : dat[1].str.contains("E"),
        "stiF" : dat[1].str.contains("F")
        }
       # Testing data 
            #all tests
        
        findTest = dat[0].str.contains('testing')
            #conditions
        test_n3 = dat[1].str.contains('n3') 
        dat[1].str.contains('m3') 
        test_n6 = dat[1].str.contains('n6') 
        dat[1].str.contains('m6')
        
    # Extract and align and order randomly presented stims for averaging
        acc_m3 = pd.DataFrame()
        acc_m6 = pd.DataFrame()
        acc_n3 = pd.DataFrame()
        acc_n6 = pd.DataFrame()

        for c in findCond:

            for s in findStim:
                if c ==('m6'):
                    acc_m6.insert(0,s,np.array(dat.loc[findCond[c] & findStim[s], 2]), True)

                if c ==('n6'):
                    acc_n6.insert(0,s,np.array(dat.loc[findCond[c] & findStim[s], 2]), True)

                if c.endswith('3'):
                    if s.endswith('D') | s.endswith('E') | s.endswith('F'):
                        continue
                if c == ('m3'):
                    acc_m3.insert(0,s,np.array(dat.loc[findCond[c] & findStim[s], 2]), True)

                if c == ('n3'):
                    acc_n3.insert(0,s,np.array(dat.loc[findCond[c] & findStim[s], 2]), True)

        # Reshape and average

        subject_data.update( {(fl[-8:-4]) : {'n3': np.array(acc_n3).reshape([13, 12],order='F').mean(axis=1),
                  'm3': np.array(acc_m3).reshape([13, 12],order='F').mean(axis=1),
                  'n6': np.array(acc_n6).reshape([13, 18],order='F').mean(axis=1),
                  'm6': np.array(acc_m6).reshape([13, 18],order='F').mean(axis=1),
                  'test3' : np.array(dat.loc[findTest & test_n3, 2]).mean(),
                  'test6' : np.array(dat.loc[findTest & test_n6, 2]).mean()
                                            }
                             }
                           )

    return subject_data


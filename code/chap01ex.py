"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function

import numpy as np
import sys

import nsfg
import thinkstats2

# RW: This is just a direct copy of Downey's provided function.
# I've decided not to get bogged down in the low level utility mechanics
# in my study in this book. My purpose is learning statists theory and algorithms 
# and ideomatic python generally. Just use whatever utility methods are provided
# in thinkstats2 module, review them for general familiarity, and keep moving
# forward through the material.
def ReadFemResp(dct_file='2002FemResp.dct',
                dat_file='2002FemResp.dat.gz',
                nrows=None):
    """Reads the NSFG respondent data.

    dct_file: string file name
    dat_file: string file name

    returns: DataFrame
    """
    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression='gzip', nrows=nrows)
    CleanFemResp(df) # only pass so far
    return df

# NoOp so far
def CleanFemResp(df):
    """Recodes variables from the respondent frame.

    df: DataFrame
    """
    pass

# This is a copy of the ValidatePregnum function in chap01soln.py.
# The objective here is to analyze and annotate it to learn from it.
def ValidatePregnum(resp):
    """Validate pregnum in the respondent file.

    resp: respondent DataFrame
    """
    # read the pregnancy frame
    preg = nsfg.ReadFemPreg()
    
    # [RW: Ok, my suppostion is that resp is the full femResp2002 df,
    #  and preg is the full femPreg2002 df (per my file chap01_2_1ex.ipynb).]

    # make the map from caseid to list of pregnancy indices
    preg_map = nsfg.MakePregMap(preg)
    
    # iterate through the respondent pregnum series
    # 7643 records
    # Each record is a unique caseid and each pregnum is the total number of 
    # corresponding pregnancies.
    for index, pregnum in resp.pregnum.items():
        caseid = resp.caseid[index] # getting the corresponding caseid for this/each record.
        indices = preg_map[caseid]

        # check that pregnum from the respondent file equals
        # the number of records in the pregnancy file
        # [RW: This implementation can only identify the first inequality and then stops.
        #  Would be better to keep going and identify all inequalities. But the
        #  inference is that in terms of cross-validation, if there is even a single discrepancy,
        #  then the data is not validated. Perhaps patterns can still be identified this way.
        #  It's a start.]
        if len(indices) != pregnum:
            print(caseid, len(indices), pregnum)
            return False

    return True # pregnum data is cross-validated.

def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    
    print('%s: All tests passed.' % script)

if __name__ == '__main__':
    main(*sys.argv)

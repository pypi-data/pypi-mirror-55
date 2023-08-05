#!/usr/bin/env python
# coding: utf-8

# In[15]:


import unittest
import pandas
import numpy as np

l = [ { "date":"2014-06-22", "prix":220.0, "devise":"euros", "indice": 450}, { "date":"2014-06-23", "prix":221.0, "devise":"euros", "indice": 1548},
     { "date":"2014-06-23", "prix":225.0, "devise":"euros", "indice": 700}, { "date":"2014-06-23", "prix":224.0, "devise":"euros", "indice": 30}]
df = pandas.DataFrame(l)


def get_se(df):
            res = []
            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            for var in list(df):
                if df[var].dtypes in numerics:
                    res.append(df[var].var())
                else:
                    res.append(np.nan)
            return res

def get_min(df):
            res = []
            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            for var in list(df):
                if df[var].dtypes in numerics:
                    res.append(df[var].min())
                else:
                    res.append(np.nan)
            return res

def get_max(df):
            res = []
            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            for var in list(df):
                if df[var].dtypes in numerics:
                    res.append(df[var].max())
                else:
                    res.append(np.nan)
            return res

def get_occ_et_val_princi(df):
            res = []
            l=[]
            j=0
            for i in df.columns:
                l = list(df[i].value_counts().to_dict().items())[:min(3, len(df[i].value_counts()))]
                res.append(l)
               # for j in range(len(list(df[i].value_counts().to_dict().items())[:min(3, len(df[i].value_counts()))])):
               #     res.append(l[j])
            return res

class PAE_Test(unittest.TestCase):

    def setUp(self):
        self.tableau = df
    
    def test_get_se(self) :
        vr = get_se(self.tableau)
        self.assertEqual(vr,[np.nan, 5.666666666666667, np.nan, 409736.0])
    
    def test_get_min(self) :
        mi = get_min(self.tableau)
        self.assertEqual(mi,[np.nan, 220.0, np.nan, 30])
    
    def test_get_max(self) :
        mx = get_max(self.tableau)
        self.assertEqual(mx,[np.nan, 225.0, np.nan, 1548])
    
    def test_get_occ_et_val_princi(self) :
        occ = get_occ_et_val_princi(self.tableau)
        self.assertEqual(occ,[[('2014-06-23', 3), ('2014-06-22', 1)],[(224.0, 1), (225.0, 1), (221.0, 1)],[('euros', 4)],[(30, 1), (1548, 1), (700, 1)]]) 
        
unittest.main(argv=[''], verbosity=2, exit=False)


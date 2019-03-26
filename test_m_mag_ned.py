import numpy as np
from ddt import ddt, data, unpack
from math import acos, cos, sin, pi
import unittest
from pyigrf12 import runigrf12
from datetime import *

'''
    This is test code for checking magfield output csv file. 
    Unlike typical test-codes it does not check equality.
    It prints the fractional error between one-obtained from websites and one obtained from our igrf. 
    (check QA-doc for link to those websites) 
'''
#Befor running this test-code you need to run m_mag_ned.py 
# and change lla = np.genfromtxt('LLA.csv', delimiter=",") to lla = np.genfromtxt('LLA_m_mag_ned_test.csv',delimiter=",")    

@ddt
class Test_magfield(unittest.TestCase):
    
    m_mag_ned = np.genfromtxt('mag_output_ned.csv',delimiter=",") 
    m_mag_test_reference = np.genfromtxt('m_mag_ned_test_reference.csv',delimiter=",")
    
    def test_magfield_predata(self):
        print((self.m_mag_ned[:,1:4]-self.m_mag_test_reference[:,0:3])/self.m_mag_ned[:,1:4])

if __name__=='__main__':
   unittest.main(verbosity=2)
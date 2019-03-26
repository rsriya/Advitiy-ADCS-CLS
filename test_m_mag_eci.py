import numpy as np
from constants_1U import W_EARTH, R_EARTH
from ddt import ddt, data, unpack
from math import acos, cos, sin, pi
import unittest

'''
	This is test code for checking magfield output csv file. 
'''

EPOCH = dt.datetime(2018, 4, 3, 12, 50, 19)	#date of launch t=0
EQUINOX = dt.datetime(2018, 3, 20, 13, 5, 00)	#day of equinox

@ddt
class Test_magfield(unittest.TestCase):
	
	magoutput_ned = np.genfromtxt('mag_output_ned.csv',delimiter=",")	
	magoutput_i = np.genfromtxt('mag_output_i.csv',delimiter=",")	
	LLA = np.genfromtxt('LLA.csv',delimiter=",")
	t0 = (EPOCH - EQUINOX).total_seconds()
	T = magoutput_ned[:,0]
	v_result = np.zeros(4)
	l = np.linspace(0,len(T),10,int)	#Sample data points from entire file
	
	@data(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9])
	
	def test_magfield_rundata(self,value):
		theta = (90 - self.LLA[int(value)-1, 1]) * pi/180
		if (self.LLA[int(value)-1, 2] >= 0):
			phi = (self.LLA[int(value)-1, 2]) * pi/180
		else:
			phi = (self.LLA[int(value)-1, 2] + 360) * pi/180
		m_DCMn2e = np.array([[-1*cos(theta)*cos(phi), -1*sin(phi), -1*sin(theta)*cos(phi)], [-1*cos(theta)*sin(phi), cos(phi),-1*sin(theta)*sin(phi)], [sin(theta),0.,-1*cos(theta)]])
		magoutput_e = np.dot(m_DCMn2e,self.magoutput_ned[int(value)-1,1:4])
		
		theta = W_EARTH*(self.t0 + self.magoutput_ned[int(value)-1,0]) #in radian
		m_DCMe2i = np.array([[cos(theta), -1*sin(theta), 0.], [sin(theta), cos(theta),0.], [0.,0.,1.]])
		self.v_result[0] = self.magoutput_ned[int(value)-1,0]
		self.v_result[1:4] = np.dot(m_DCMe2i,magoutput_e)
		self.magoutput_i[int(value)-1,:]
		self.assertTrue(np.allclose(self.magoutput_i[int(value)-1,:],self.v_result))
	
	
	magoutput_i_test = np.genfromtxt('mag_output_i_test.csv',delimiter=",")	
	LLAtest = np.genfromtxt('LLA_test_for_magfield.csv',delimiter=",")
	magoutput_ned_test = np.genfromtxt('mag_output_ned_test.csv',delimiter=",")
	@data(0,1,2,3,4,5,6,7)	
	def test_GetLLA_predefined_data(self,value):
		theta = (90 - self.LLAtest[int(value), 1]) * pi/180
		if (self.LLAtest[int(value), 2] >= 0):
			phi = (self.LLAtest[int(value), 2]) * pi/180
		else:
			phi = (self.LLAtest[int(value), 2] + 360) * pi/180
		m_DCMn2e = np.array([[-1*cos(theta)*cos(phi), -1*sin(phi), -1*sin(theta)*cos(phi)], [-1*cos(theta)*sin(phi), cos(phi),-1*sin(theta)*sin(phi)], [sin(theta),0.,-1*cos(theta)]])
		magoutput_e = np.dot(m_DCMn2e,self.magoutput_ned_test[int(value),1:4])
		
		theta = W_EARTH*(self.t0 + self.magoutput_ned_test[int(value),0]) #in radian
		m_DCMe2i = np.array([[cos(theta), -1*sin(theta), 0.], [sin(theta), cos(theta),0.], [0.,0.,1.]])
		self.v_result[0] = self.magoutput_ned[int(value),0]
		self.v_result[1:4] = np.dot(m_DCMe2i,magoutput_e)
		self.assertTrue(np.allclose(self.magoutput_i_test[int(value),:],self.v_result))
	
if __name__=='__main__':
   unittest.main(verbosity=2)
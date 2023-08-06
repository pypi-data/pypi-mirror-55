import math, numba 


@numba.njit
def Flux_drop_uniform( z, k, SBR):
    if (z >= 1. + k) or ((z >= 1.) and  (z <= k - 1.)) :  return 0.0           # total eclipse of the star
    elif  (z <= 1. - k)                                :  return - SBR*k*k   # planet is fully in transit		
    else :                                                                     #  planet is crossing the limb
        kap1 = math.acos(min((1. - k*k + z*z)/2./z, 1.))
        kap0 = math.acos(min((k*k + z*z - 1.)/2./k/z, 1.))
        return - SBR*  (k*k*kap0 + kap1 - 0.5*math.sqrt(max(4.*z*z - math.pow(1. + z*z - k*k, 2.), 0.)))/math.pi 


'''
import numpy as np 
import matplotlib.pyplot as plt 
z = np.linspace(-2,2,1000) 
_z = np.abs(z)
k = 0.1
SBR = 0.4 


for i in range(len(z)) : plt.scatter(z[i], Flux_drop_uniform( _z[i], k, SBR)) 
plt.show()
'''
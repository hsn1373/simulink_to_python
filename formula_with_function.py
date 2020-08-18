from math import *
import matplotlib.pyplot as plt

#**************************************************************************
#**************************************************************************
#**************************************************************************

def Integral(Input,first_output,delta_t):

    Integral_result=[first_output]

    for i in range(1,len(Input)):
        Integral_result.append(Integral_result[i-1]+(Input[i]*delta_t))

    return Integral_result

#**************************************************************************
#**************************************************************************
#**************************************************************************

def Diff(Input,first_output,delta_t):

    diff_result=[first_output]

    for i in range(1,len(Input)):
        diff_result.append((Input[i]-Input[i-1])/delta_t)

    return diff_result

#**************************************************************************
#**************************************************************************
#**************************************************************************


#******************************* Main *************************************

input_data=[]
delta_t=0.001

t=0
while t<1:
    input_data.append(sin(2*pi*t))
    t+=delta_t


plt.plot(input_data,'b-',Integral(input_data,0,delta_t),'r-',Diff(input_data,0,delta_t),'g-')
plt.show()

#******************************* Main *************************************
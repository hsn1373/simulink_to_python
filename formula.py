from math import *
import matplotlib.pyplot as plt

input_data=[]
delta_t=0.001
pervious_integral=0
Integral_result=[0]
diff_result=[0]

cos_data=[]

t=0
while t<1:
    input_data.append(sin(2*pi*t))
    t+=delta_t

t=0
while t<1:
    cos_data.append((-1/(2*pi))*(cos(2*pi*t) - 1))
    # cos_data.append(2*pi*cos(2*pi*t))
    t+=delta_t


for i in range(1,len(input_data)):
    Integral_result.append(Integral_result[i-1]+(input_data[i]*delta_t))

for i in range(1,len(input_data)):
    diff_result.append((input_data[i]-input_data[i-1])/delta_t)



plt.plot(input_data,'b-',Integral_result,'r-',diff_result,'g-')
plt.show()

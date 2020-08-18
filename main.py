# import threading
from math import *
from scipy.io import loadmat
import xlsxwriter
import time


#**************************************************************************
#**************************************************************************
#**************************************************************************


def printit():
  threading.Timer(0.001, printit).start()
  print ("Hello, World!")



#**************************************************************************
#**************************************************************************
#**************************************************************************


def Integral(Input,pervious_integral,delta_t):

  return pervious_integral+(Input*delta_t)


#**************************************************************************
#**************************************************************************
#**************************************************************************

def Diff(Input,pervious_input,delta_t):

  return (Input-pervious_input)/delta_t

#**************************************************************************
#**************************************************************************
#**************************************************************************

def zero_impedance(thd, thm1, thm2, tau_int1, tau_int2, th_tild1, th_tild2, th_tild1_dt, th_tild2_dt, Cte):

    m0 = Cte[0]
    c0 = Cte[1]
    k0 = Cte[2]
    gamma_m = Cte[3]
    gamma_c = Cte[4]
    gamma_k = Cte[5]
    # tau_int = [tau_int1*0.2575,tau_int2*0.2575]
    tau_int = [tau_int1,tau_int2]

    e1 = thd[0] - thm1
    e2 = thd[1] - thm2

    alpha = 0.001
    beta = 0.02

    SM_r = 1 / (alpha*(e1**2) + beta*(tau_int[0]**2) + 1)
    SM_l = 1 / (alpha*(e2**2) + beta*(tau_int[1]**2) + 1)

    m1_d = m0 + gamma_m*(1 - 2*SM_r)
    c1_d = c0 + gamma_c*(1 - 2*SM_r)
    k1_d = k0 + gamma_k*(1 - 2*SM_r)
    m2_d = m0 + gamma_m*(1 - 2*SM_l)
    c2_d = c0 + gamma_c*(1 - 2*SM_l)
    k2_d = k0 + gamma_k*(1 - 2*SM_l)

    th_tild1_ddt = 1/m1_d * (tau_int[0] - c1_d*th_tild1_dt - k1_d*th_tild1)
    th_tild2_ddt = 1/m2_d * (tau_int[1] - c2_d*th_tild2_dt - k2_d*th_tild2)

    # print(th_tild1_ddt," * ",th_tild2_ddt)

    return th_tild1_ddt, th_tild2_ddt, m1_d, m2_d, c1_d, c2_d, k1_d, k2_d, SM_r, SM_l

#**************************************************************************
#**************************************************************************
#**************************************************************************

def Assist_control(theta_hip, theta_hip_dt, thd, thd_dt, thd_ddt, th_tild1, th_tild2,th_tild1_dt, th_tild2_dt,th_tild1_ddt, th_tild2_ddt, tau_int1, tau_int2, mxlak):


  max_torque=mxlak[0]
  lambd=mxlak[1]
  k=mxlak[2]
  # tau_int = [tau_int1*0.257, tau_int2*0.257]
  tau_int = [tau_int1, tau_int2]

  theta_i = [thd[0]+th_tild1, thd[1]+th_tild2]
  theta_i_dt = [thd_dt[0]+th_tild1_dt, thd_dt[1]+th_tild2_dt]
  theta_i_ddt = [thd_ddt[0]+th_tild1_ddt, thd_ddt[1]+th_tild2_ddt]

  g = 9.81

  mass_r = 0.8 + 0.45 + 0.52

  l_r = 0.2575

  Ir = 0.05 + (3.5+0.09)*0.0001

  Gr = [mass_r * g * l_r * sin(theta_hip[0]) / 2,mass_r * g * l_r * sin(theta_hip[1]) / 2]
  Mr = Ir
  Cr = 0.001124

  e = [theta_hip[0] - theta_i[0],theta_hip[1] - theta_i[1]]
  e_dt = [theta_hip_dt[0] - theta_i_dt[0],theta_hip_dt[1] - theta_i_dt[1]]


  s = [e_dt[0] + lambd*e[0],e_dt[1] + lambd*e[1]]
  w = [theta_i_dt[0] - lambd * e[0],theta_i_dt[1] - lambd * e[1]]
  w_dt = [theta_i_ddt[0] - lambd * e_dt[0],theta_i_ddt[1] - lambd * e_dt[1]]

  if(s[0]>0):
    sign_s_1=1
  elif(s[0]<0):
    sign_s_1=-1
  else:
    sign_s_1=0

  if(s[1]>0):
    sign_s_2=1
  elif(s[1]<0):
    sign_s_2=-1
  else:
    sign_s_2=0

  F = [Mr*w_dt[0] + Cr*(w[0]+s[0]) + Gr[0] - k*s[0] - 5*sign_s_1 + tau_int[0] , Mr*w_dt[1] + Cr*(w[1]+s[1]) + Gr[1] - k*s[1] - 5*sign_s_2 + tau_int[1]]

  F_SMA_R = F[0] * 1000/16
  F_SMA_L = F[1] * 1000/16

  if(F_SMA_R > max_torque):
    F_SMA_R = max_torque
  elif(F_SMA_R < -max_torque):
    F_SMA_R = -max_torque

  if(F_SMA_L > max_torque):
    F_SMA_L = max_torque
  elif(F_SMA_L < -max_torque):
    F_SMA_L = -max_torque

  return F_SMA_R,F_SMA_L





#**************************************************************************
#**************************************************************************
#**************************************************************************


#******************************* Main *************************************

#*************
#initialize inputs

pervious_teta_1=0
pervious_teta_dot_1=0
pervious_teta_2=0
pervious_teta_dot_2=0
pervious_theta_hip=[0,0]

Cte=[3,60,100,2,4,20]
mxlak=[1000,80,0.05]

thd_file = loadmat('thd.mat')
thd_dt_file = loadmat('thd_dt.mat')
thd_ddt_file = loadmat('thd_ddt.mat')
input_1 = loadmat('in1.mat')
input_2 = loadmat('in2.mat')
input_3 = loadmat('in3.mat')
input_4 = loadmat('in4.mat')
i=0
delta_t=0.0005
pulse_to_radian=2*pi/4096/50/4

final_result_array1=[]
final_result_array2=[]

test_array=[]
test_array2=[]

#*************

start_time = time.time()

while True:

  if(i==len(thd_file['Data'])):
    # workbook = xlsxwriter.Workbook('test_Result1.xlsx') 
    # worksheet = workbook.add_worksheet()

    # for j in range(len(final_result_array1)):
    #   worksheet.write(j, 0, final_result_array1[j])
    #   worksheet.write(j, 1, final_result_array2[j])
    #   # worksheet.write(j, 0, test_array[j])
    #   # worksheet.write(j, 1, test_array2[j])
    # workbook.close() 

    break

  thd=[thd_file['Data'][i][0],thd_file['Data'][i][1]]
  thm1=input_3['Data'][i][0]
  thm2=input_4['Data'][i][0]
  tau_int1=input_1['Data'][i][0]
  tau_int2=input_2['Data'][i][0]
  th_tild1=pervious_teta_1
  th_tild2=pervious_teta_2
  th_tild1_dt=pervious_teta_dot_1
  th_tild2_dt=pervious_teta_dot_2


  result=zero_impedance(thd, thm1, thm2, tau_int1, tau_int2, th_tild1, th_tild2, th_tild1_dt, th_tild2_dt, Cte)

  pervious_teta_dot_1=Integral(result[0],pervious_teta_dot_1,delta_t)
  pervious_teta_1=Integral(pervious_teta_dot_1,pervious_teta_1,delta_t)
  pervious_teta_dot_2=Integral(result[1],pervious_teta_dot_2,delta_t)
  pervious_teta_2=Integral(pervious_teta_dot_2,pervious_teta_2,delta_t)


  # test_array.append(result[0])
  # test_array2.append(result[1])
  # test_array.append(pervious_teta_dot_1)
  # test_array2.append(pervious_teta_1)



  #*************************************

  theta_hip=[pulse_to_radian*input_3['Data'][i][0],pulse_to_radian*input_4['Data'][i][0]]
  theta_hip_dt=[Diff(theta_hip[0],pervious_theta_hip[0],delta_t),Diff(theta_hip[1],pervious_theta_hip[1],delta_t)]
  pervious_theta_hip=theta_hip

  thd_dt=[thd_dt_file['Data'][i][0],thd_dt_file['Data'][i][1]]
  thd_ddt=[thd_ddt_file['Data'][i][0],thd_ddt_file['Data'][i][1]]

  final_result=Assist_control(theta_hip, theta_hip_dt, thd, thd_dt, thd_ddt, pervious_teta_1, pervious_teta_2,pervious_teta_dot_1, pervious_teta_dot_2,result[0], result[1], tau_int1, tau_int2, mxlak)

  # print(final_result[0]," * ",final_result[1])
  # final_result_array1.append(final_result[0])
  # final_result_array2.append(final_result[1])



  i+=1
  # time.sleep(delta_t - ((time.time() - starttime) % delta_t))


print("--- %s seconds ---" % (time.time() - start_time))

#******************************


# printit()

#******************************* Main *************************************
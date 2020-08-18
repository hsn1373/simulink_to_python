from scipy.io import loadmat
from math import *
import xlsxwriter



def Integral(x0,x1,x2,Input,pervious_integral,delta_t):

  return pervious_integral+(3*delta_t/8*(Input+3*x2+3*x1+x0))


delta_t=0.0005
theta_ddt = loadmat('theta_ddt.mat')
x_0=0
x_1=0
x_2=0
pervious_integral=0
reslt=[]

pervious_integral=Integral(x_0,x_1,x_2,theta_ddt['Data'][0][0],pervious_integral,delta_t)
reslt.append(pervious_integral)
pervious_integral=Integral(x_0,x_1,theta_ddt['Data'][0][0],theta_ddt['Data'][1][0],pervious_integral,delta_t)
reslt.append(pervious_integral)
pervious_integral=Integral(x_0,theta_ddt['Data'][0][0],theta_ddt['Data'][1][0],theta_ddt['Data'][2][0],pervious_integral,delta_t)
reslt.append(pervious_integral)
pervious_integral=Integral(theta_ddt['Data'][0][0],theta_ddt['Data'][1][0],theta_ddt['Data'][2][0],theta_ddt['Data'][3][0],pervious_integral,delta_t)
reslt.append(pervious_integral)

for i in range(4,len(theta_ddt['Data'])):
    pervious_integral=Integral(theta_ddt['Data'][i-3][0],theta_ddt['Data'][i-2][0],theta_ddt['Data'][i-1][0],theta_ddt['Data'][i][0],pervious_integral,delta_t)
    reslt.append(pervious_integral)

workbook = xlsxwriter.Workbook('theta_dt_simp3.xlsx')
worksheet = workbook.add_worksheet()

for j in range(len(reslt)):
    worksheet.write(j, 0, reslt[j])

workbook.close() 

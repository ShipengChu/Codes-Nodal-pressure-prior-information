#This file define the global variable for the mcmc method
BurnIn_Samples=600
Total_Samples=1200
#Define the measurements
import numpy as np


Num_sensor=4
SensorID=['N9','N3','N6','L4']
Measured_value=[-82.70,29.19,25.45,20.06]
Measured_std=[1.0,0.3,0.3,1.0]

#Define the prior demand
Num_demand=8
Demand_ID=['N1','N2','N3','N4','N5','N6','N7','N8']
Prior_demand=[7.86,6.57,21.13,4.07,9.65,9.58,6.40,14.42]
Prior_std=[3.0,1.5,4.5,1.2,3.0,2.4,3.0,6.0]
DemandBoundary=[0,100]

#Define the prior pressure
NPI=2
if NPI==2: #the prior pressure is used to estimate the nodal water demand
    Pressure_Boundary=[[23,28],[15,20]]
    Prior_Pressure_ID=['N5','N8']
    Alpha_uniform=np.log(1.001)
Proposal_Type='Uniform'#'Uniform'  #'Normal'

#Define the inpfile
Inp='case 1_sim.inp'

if NPI==0: #The following parameter has been optimized to control the acceptance ratio
    Proposal_Uniform_Boundary_Ratio=0.6
    Proposal_Normal_Sigma=1
if NPI==2:
    Proposal_Uniform_Boundary_Ratio=0.05
    Proposal_Normal_Sigma=1


ResultInp='MCMC_NPI='+str(NPI)+".inp"
 


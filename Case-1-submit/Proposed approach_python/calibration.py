from Epanet_package import *
import numpy  as np
import time
import pandas as pd
Num_demand=8

def Demand_Calibration_GPU(inpfile,inputdata,resultInp,NumIters,Step):
    Demand=[0]*Num_demand
    Demand_Cov=[0]*Num_demand
    enOpen(inpfile,"buf.rtp",'')
    enInput(inputdata,GPU_CODE=1,numThreads_CPU=4)
    enInitDemandCalibration()
    enDemandCalibration(NumIters,Step)

    for i in range(Num_demand):
        index=i+1
        [errcode,demand]=enGetnodevalue(index,1)
        [errcode,cov]=enGetdemandCOV(index, index)
        Demand[i]=demand
        Demand_Cov[i]=cov

    enCloseDemandCalibration()
    enSaveinpfile(resultInp)
    enCloseInput()
    enClose()
    print('Demand calibration over')
    return Demand,Demand_Cov

start= time.clock()
for i in range(20):
    [Demand,Demand_Var]=Demand_Calibration_GPU('case 1_sim.inp', 'Proposed.obs', 'result_Proposed.inp',25, 0.25)
    print(str(i)+'  over')
end= time.clock()

print('\n\nTime consumption: '+str((end-start)*1000/20))
pd.DataFrame(Demand).to_csv('Demand.csv')
pd.DataFrame(Demand_Var).to_csv('demandVar.csv')

print('\ndemand                standard deviation')
for i in range(Num_demand):
    print(str(Demand[i])+'   '+str(Demand_Var[i]**0.5))



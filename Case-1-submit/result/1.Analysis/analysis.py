
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import math
import pandas as pd
import os
import numpy as np
from Epanet_package import *

LineWidth=3
FontSize =24

PATH=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PATH=os.path.abspath(os.path.dirname(PATH))

MCMC_NPI_2=PATH+'\\MCMC approach_python NPI=2\\result #8 obj=8.05 The best one'

Num_demand=8
NodeID=['N1','N2','N3','N4','N5','N6','N7','N8']
BurnIn_Samples=600
Total_Samples=1200

Demand_MCMC_NPI_2=pd.read_csv(MCMC_NPI_2+'\\NPI=2_waterdemand.csv')

Demand_Prior=[7.86,6.57,21.13,4.07,9.65,9.58,6.40,14.42]
Std_Prior=[3.0,1.5,4.5,1.2,3.0,2.4,3.0,6.0]

Demand_Proposed_Method=[10.18,6.34,14.28,4.08,9.66,7.77,7.90,22.17]
Std_Proposed_Method=[1.37,1.46,1.44,0.97,2.33,0.59,2.67,2.36]

Demand_Bayesian_Method=[11.40,6.54,16.11,4.70,9.78,8.51,7.66,17.43]
Std_Bayesian_Method=[1.65,1.47,2.01,1.08,2.85,0.75,2.71,4.35]

Range=[[4,18],[0,12],[10,22],[0,8],[0,20],[0,15],[0,18],[5,30]]


aveDemand_NPI_2=0
Result_NPI_2=[]

print('    aveDemand_NPI_2   aveStd_NPI_2')
for demand_index in range(Num_demand):

    Result_oneNode_NPI_2=[]
    Result_oneNode_NPI_2.append(NodeID[demand_index])

    title=NodeID[demand_index]
    plt.rc('font',family='Times New Roman')
    fig=plt.figure(dpi=128*2,figsize=(7,12))#figsize=(12,7)
    ax = fig.add_subplot(111)
    plt.tick_params(labelsize=FontSize)
 

    demand_NPI_2=Demand_MCMC_NPI_2[str(demand_index)].tolist()[BurnIn_Samples:Total_Samples]



    aveDemand_NPI_2=np.average(demand_NPI_2)
    aveStd_NPI_2=np.std(demand_NPI_2)

 
    plt.hist(demand_NPI_2,range=Range[demand_index],label='MCMC s=2', bins=200, density=True, color='blue', alpha=0.6)

    x=np.linspace(Range[demand_index][0], Range[demand_index][1], 100)

    mu_Prior=Demand_Prior[demand_index]
    sigma_Prior=Std_Prior[demand_index]
    y_Prior = ((1/(np.power(2*np.pi, 0.5)*sigma_Prior))*np.exp(-0.5*np.power((x-mu_Prior)/sigma_Prior, 2)))
    ax.plot(x, y_Prior, color="black", ls="--", linewidth=LineWidth,label='Prior', alpha=0.8)

    mu_Bayesian=Demand_Bayesian_Method[demand_index]
    sigma_Bayesian=Std_Bayesian_Method[demand_index]
    y_Bayesian = ((1/(np.power(2*np.pi, 0.5)*sigma_Bayesian))*np.exp(-0.5*np.power((x-mu_Bayesian)/sigma_Bayesian, 2)))
    ax.plot(x, y_Bayesian, color="green", ls="-", linewidth=LineWidth,label='Bayesian s=0')

    mu_Proposed=Demand_Proposed_Method[demand_index]
    sigma_Proposed=Std_Proposed_Method[demand_index]
    y_Proposed = ((1/(np.power(2*np.pi, 0.5)*sigma_Proposed))*np.exp(-0.5*np.power((x-mu_Proposed)/sigma_Proposed, 2)))
    ax.plot(x, y_Proposed, color="red", ls="-", linewidth=LineWidth,label='Proposed s=2')
    
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))#纵坐标保留一位小数

    plt.legend(loc='upper right',fontsize =FontSize)
    plt.xlabel('Nodal water demand (L/s)',fontsize =FontSize)
    plt.ylabel('Probability density',fontsize =FontSize)
    plt.title(title,fontsize =FontSize,x=0.2, y=0.8,color="black")
    plt.savefig(title+'.jpg') 

    printStr=title+'  {:.2f}'.format(np.average(aveDemand_NPI_2))+'              '+'{:.2f}'.format(np.average(aveStd_NPI_2))

    Result_oneNode_NPI_2.append(np.average(aveDemand_NPI_2))
    Result_oneNode_NPI_2.append(np.average(aveStd_NPI_2))
    
    Result_NPI_2.append(Result_oneNode_NPI_2)
    print(printStr)

enOpen('case 1_sim.inp', '1.rtp', '')


for i in range(Num_demand):
    id=Result_NPI_2[i][0]
    value=Result_NPI_2[i][1]
    [errcode,index]=enGetnodeIndex(id)
    errcode=enSetnodevalue(index, 1, value)
enSaveinpfile('MCMC_NPI_2.inp')

    







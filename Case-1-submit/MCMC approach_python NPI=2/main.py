from Probability_model import *
from Global_variable import *
import math
import pandas as pd
from MCMC import *
from Epanet_package import *
import time
import matplotlib.pyplot as plt

start=time.clock()
MCMC_model=MCMC_model(Proposal_type=Proposal_Type,proposal_sigma=Proposal_Normal_Sigma,proposal_uniform_boundary_ratio=Proposal_Uniform_Boundary_Ratio,nSamples=Total_Samples)
[Waterdemand,Para_optim]=MCMC_model.MCMC_sampling()
end= time.clock()
print('\n\nTime consumption: '+str((end-start)*1000))

df1=pd.DataFrame(Waterdemand)
df1.to_csv('NPI='+str(NPI)+'_waterdemand.csv')

df2=pd.DataFrame(Para_optim)
df2.to_csv('NPI='+str(NPI)+'_Para_optim.csv')


Obj_sample=[]
for sample_index in range(BurnIn_Samples,Total_Samples):
    Obj_sample.append(Para_optim[sample_index][1])
    
print('Average Obj: {:.2f}'.format(np.average(Obj_sample)))
print('Average acceptance ratio: {:.4f}'.format(np.average(df2[2])))
print('The parameter in the proposal distribuiton should be adjusted to make the ratio approach to 0.23')
print()
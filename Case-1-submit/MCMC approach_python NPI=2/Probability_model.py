
import numpy as np
from Global_variable import *
from Epanet_package import *
import math


def feasibilityEvaluation(sample):
    demand=sample.tolist()[0]
    flag=[0,0]
    errcode=enOpen(Inp, 'case1.rtp', '')
    for i in range(Num_demand):
        node_index=i+1
        errcode=enSetnodevalue(node_index, 1, demand[i])
    errcode=enSolveH()

    
     
    for i in range(NPI):
        [errcode,node_index]=enGetnodeIndex(Prior_Pressure_ID[i])
        [errcode,pressure]=enGetnodevalue(node_index,11)
        if pressure<Pressure_Boundary[i][0]:
            flag[i]=-1
        if pressure>Pressure_Boundary[i][1]:
            flag[i]=1   
    enClose()
    return flag


def getResultInpfile(waterDemand):
    errcode=enOpen(Inp, 'result.rtp', '')
    for i in range(Num_demand):
        enSetnodevalue(i+1, 1, waterDemand[i])
    enSaveinpfile(ResultInp)
    errrcode=enSolveH()
    print('\n\nid  demand       pressure')
    for i in range(Num_demand):
        [errcode,id]=enGetnodeID(i+1)

        [errcode,pressure]=enGetnodevalue(i+1, 11)
        print(id+': '+str(format(waterDemand[i], '.2f'))+'       '+str(format(pressure, '.2f')))
    enClose()
    print('\n\n')

    
def samplingPrior_probability():
    
    mean=np.array(Prior_demand)
    cov=[0]*Num_demand
    for i in range(Num_demand):
        cov[i]=Prior_std[i]**2
    cov=np.diag(cov)

    sample=np.random.multivariate_normal(mean, cov, (1,), 'raise')

    for i in range(sample.shape[1]):
        if sample[0][i]<0 or sample[0][i]>30:
            sample[0][i]=15 #

    #evaluate the feasibility of the sample
    if NPI>0:
        flag=feasibilityEvaluation(sample)

        ff1=(flag[0]<0 and flag[1]<=0) or (flag[0]<=0 and flag[1]<0)
        while ff1:
            sample=sample*0.999
            flag=feasibilityEvaluation(sample)
            ff1=(flag[0]<0 and flag[1]<=0) or (flag[0]<=0 and flag[1]<0)
            if (ff1!=1):
                    break

        ff2=(flag[0]>0 and flag[1]>=0) or (flag[0]>=0 and flag[1]>0)
        while ff2:#the initial demand is too small  to match the prior pressure
            sample=sample*1.001
            flag=feasibilityEvaluation(sample)
            ff2=(flag[0]>0 and flag[1]>=0) or (flag[0]>=0 and flag[1]>0)
            if (ff2!=1):
                break


        ff3=(flag[0]*flag[1]<0)
        if ff3:
            print('failed to initialize the sample')

    return sample[0]




class Probability_model(object):
    
    def __init__(self, Water_demand):

        self.Water_demand = np.asarray(Water_demand)
        self.sim_measured_reslut=[0]*Num_sensor
        self.sim_pressure_prior_result=[0]*NPI

    def getHydSimResult(self):
        errcode=enOpen(Inp, 'case1.rtp', '')
        for i in range(Num_demand):
            node_index=i+1
            errcode=enSetnodevalue(node_index, 1, self.Water_demand[i])
        errcode=enSolveH()

        sim_measured_reslut=[0]*len(SensorID)
        sim_pressure_prior_result=[0]*NPI

        [errcode,node_index]=enGetnodeIndex(SensorID[0])
        [errcode,sim_measured_reslut[0]]=enGetnodevalue(node_index, 9)#get the tankflow for the #1 sensor

        for i in range(1,3,1): #get the nodal pressure for the #2 and #3 sensors
            [errcode,node_index]=enGetnodeIndex(SensorID[i])
            [errcode,sim_measured_reslut[i]]=enGetnodevalue(node_index,11)

        [errcode,link_index]=enGetlinkIndex(SensorID[3])
        [errcode,sim_measured_reslut[3]]=enGetlinkvalue(link_index, 8) #get the pipe flow for the #4 sensor
        
        for i in range(NPI):
            [errcode,node_index]=enGetnodeIndex(Prior_Pressure_ID[i])
            [errcode,sim_pressure_prior_result[i]]=enGetnodevalue(node_index,11)
        
        enClose()
        self.sim_measured_reslut=sim_measured_reslut
        self.sim_pressure_prior_result=sim_pressure_prior_result


    def ln_likelihood(self):
        inv_var=[0]*Num_sensor
        for i in range(Num_sensor):
            inv_var[i]=1/(Measured_std[i]**2)
        inv_var=np.diag(inv_var)

        resid=np.array(self.sim_measured_reslut)-np.array(Measured_value)
        resid=resid.reshape(Num_sensor,1)
        obj1=(resid.T).dot(inv_var)
        obj1=obj1.dot(resid)
        ln_likelihood=-0.5*obj1
        return [ln_likelihood,obj1]


    def ln_prior_pressure(self):
        obj2=0# the objective value is not considered
        if NPI==0:
            return [0,obj2] #ln(1)==0

        probability=1
        for i in range(NPI):
            sim_pressure=self.sim_pressure_prior_result[i]
            low=Pressure_Boundary[i][0]
            up=Pressure_Boundary[i][1]
            if sim_pressure<=low or sim_pressure>=up:
                return [-np.inf,obj2]#the probability p=0 and ln p is negative infinite
            else:
                probability=1/(up-low)*probability
                obj2=obj2+Alpha_uniform*(1/(sim_pressure-low)-1/(sim_pressure-up))

        return [np.log(probability),obj2]


    def ln_prior_demand(self):
        inv_var=[0]*Num_demand
        for i in range(Num_sensor):
            inv_var[i]=1/(Prior_std[i]**2)
        inv_var=np.diag(inv_var)

        resid=np.array(self.Water_demand)-np.array(Prior_demand)
        resid=resid.reshape(Num_demand,1)
        obj3=(resid.T).dot(inv_var)
        obj3=obj3.dot(resid)
        ln_prior_demand=-0.5*obj3
        return [ln_prior_demand,obj3]


    def ln_posterior(self):
        self.getHydSimResult()
        [likelihood,obj1]=self.ln_likelihood()
        [prior_pressure,obj2]=self.ln_prior_pressure()
        [prior_demand,obj3]=self.ln_prior_demand()
        return [likelihood+prior_pressure+prior_demand,obj1+obj2+obj3]


def compute_ln_probability(Water_demand):
    Prob_model=Probability_model(Water_demand)
    
    [ln_posterior,obj]=Prob_model.ln_posterior()
    if np.isnan(ln_posterior[0][0]):
        print("the Ln posterior is nan")
    return [ln_posterior[0][0],obj[0][0]]

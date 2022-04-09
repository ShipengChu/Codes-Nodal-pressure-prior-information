from Probability_model import *
from Global_variable import *
import math
import numpy as np
import copy


class MCMC_model(object):
    def __init__(self, Proposal_type='Uniform',proposal_sigma=1,proposal_uniform_boundary_ratio=0.3,nSamples=1000):

        self.proposal_normal_sigma=proposal_sigma#hyper-parameter rule the acceptance ratio
        self.proposal_uniform_boundary_ratio=proposal_uniform_boundary_ratio#hyper-parameter rule the acceptance ratio
        self.Proposal_type=Proposal_type
        self.nSamples=nSamples
        
    def sample_proposal(self,mean):
        if self.Proposal_type=='Normal':
            return np.random.normal(mean, self.proposal_normal_sigma)

        if self.Proposal_type=='Uniform':
            low_boudary=(1-self.proposal_uniform_boundary_ratio)*mean
            high_boundary=(1+self.proposal_uniform_boundary_ratio)*mean
            return np.random.uniform(low=low_boudary, high=high_boundary, size=1)[0]

    def MCMC_sampling(self):
        """
        Uniform and normal probability distribution are selected as the proposal distribuiton.
        The above two distributions are symmetric and thus the calculation of acceptance ratio can be simplified.
        """

        Para_optim=np.zeros((self.nSamples,3))
        Waterdemand=np.zeros((self.nSamples+1,Num_demand)) #the nodal water demand at each iteration
        demandCurrent=samplingPrior_probability() #initialize the nodal water demand from prior PDF
        [ln_pCurrent,objCurrent]=compute_ln_probability(demandCurrent)
        print("Init demand Ln probability: "+str(ln_pCurrent))
        #demandCurrent=[10]*Num_demand
        #demandCurrent=Prior_demand

        t=0
        Waterdemand[0]=copy.deepcopy(demandCurrent)

        for t in range(self.nSamples):
            t=t+1
            
            acceptRatio=0

            [ln_pCurrent,objCurrent]=compute_ln_probability(demandCurrent)#ln probability for the current point
            for iD in range(Num_demand):#Component-wise Metropolis-Hastings  https://theclevermachine.wordpress.com/tag/metropolis-hastings-sampling/
                
                demandStar=copy.deepcopy(demandCurrent)
                demandStar[iD]=copy.deepcopy(self.sample_proposal(demandCurrent[iD]))#sample the iD-th demand from proposal PDF 
                if(abs(demandStar[iD])>1000):
                    print('error in sample demands')
                [ln_pStar,objStar]=compute_ln_probability(demandStar) #ln probability for the new point

                alpha=0
                if (ln_pStar-ln_pCurrent)>0:#(exp(ln_p1-ln_p2)>1), alpha=min[1,exp(ln_p1-ln_p2)]=1
                    alpha=1
                else:#(exp(ln_p1-ln_p2)<1), alpha=min[1,exp(ln_p1-ln_p2)]=exp(ln_p1-ln_p2)
                    alpha=math.exp(ln_pStar-ln_pCurrent)
                

                if np.random.uniform(0,1)<alpha:
                    demandCurrent=copy.deepcopy(demandStar)
                    acceptRatio=acceptRatio+1/Num_demand
                    ln_pCurrent=ln_pStar
                    objCurrent=objStar

            Waterdemand[t]=copy.deepcopy(demandCurrent)

            Para_optim[t-1]=np.array([ln_pCurrent,objCurrent,acceptRatio])
            print('Current iteration '+str(t)+': Obj '+str(objCurrent)+' ln_pCurrent '+str(ln_pCurrent)+' acceptRatio  '+str(acceptRatio))
        return [Waterdemand,Para_optim]

                
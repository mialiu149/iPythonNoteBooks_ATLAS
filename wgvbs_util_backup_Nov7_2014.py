# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>
# this version works with WgTemplates/0807_2014/, the nontight photon definition is set to be the nominal value and can not be changed.
# <codecell>
import numpy as np
from pylab import *
from uncertainties import *
from uncertainties.umath import *
from uncertainties import unumpy
## Define structure of the data to be read in, different regions.
csv_base='/Users/Mia/Documents/Work/WgZgPhysics/Analysis/WgTemplates/0603_2014/'
default_csv ='/Users/Mia/Documents/Work/WgZgPhysics/Analysis/WgTemplates/0807_2014_VeryTight/dp.csv'
def DefVars(csv_file=default_csv):
    with open(csv_file) as f:
         first_line = f.readline().strip()
         variables=first_line.split(',')
    data_obj = np.genfromtxt(csv_file, delimiter=',', skip_header=10,
           skip_footer=10, names=variables)
    return data_obj

def LoadData(csv_base='/Users/Mia/Documents/Work/WgZgPhysics/Analysis/WgTemplates/0807_2014/',measurement='inclusive',bveto=True,
             sample=['data'],process=['data'],loadedsample={'data':None},njets=0,Mjj=0,dYjj=0,dYj0_lg=999,pt_balance=0):
    print '###################################################################################################'
    print 'Loading csv files from '+csv_base
    print 'Cuts applied: njets>= ',njets,',Mjj >= ',Mjj,'GeV',',dYjj>= ',dYjj,'dYj0_lg',dYj0_lg,'pt_balance',pt_balance
    i = 0
    for f in process:
        dp = DefVars(csv_base+sample[i]+'.csv')
        data = dp
        data = data[np.where(data['dRlg']>0.4)]
        if bveto:data = data[np.where(data['bveto70']==0)]
        if f is 'zee':
           data = data[np.where(abs(data['ph_pdgId'])<50)]
           data = data[np.where(abs(data['ph_pdgId'])>0)]
        if f is 'wenu': data = data[np.where(data['fsr_veto']==0)]
        if f is 'wenugvbs' : data = data[np.where(data['bvetotruth']==0)]
        if f is 'tg' : data = data[np.where(data['bvetotruth']==1)]
        if 'inclusive' in measurement : data = data[np.where(data['njets']>=njets)]
        if 'exclusive' in measurement : data = data[np.where(data['njets']==njets)]
        loadedsample[f]=data
        #loadedsample[sample[i]]=data
        i = i+1        
    return loadedsample
############################################################
#########define your inclusive regions here#################
############################################################
def Inclusive_sig(csvfile=default_csv): 
    sample = DefVars(csv_file=csvfile)
    sample = sample[np.where(sample['MET']>35)]
    sample = sample[np.where(sample['Mt']>40)]
    sample = sample[np.where(sample['lep_iso']/sample['lep_Pt'] < 0.1)]
    sample = sample[np.where(sample['ph_istight']==1)]
    sample = sample[np.where(sample['ph_iso_cone40'] < 4)]
    return sample
def Inclusive_B(csvfile=default_csv):    
    sample = DefVars(csv_file = csvfile)
    sample = sample[np.where(sample['MET']>35)]
    sample = sample[np.where(sample['Mt']>40)]
    sample = sample[np.where(sample['lep_iso']/sample['lep_Pt'] < 0.1)]
    sample = sample[np.where(sample['ph_istight']==0)]
    sample = sample[np.where(sample['ph_iso_cone40'] > 6)]
    return sample
def Inclusive_C(csvfile=default_csv):    
    sample = DefVars(csv_file = csvfile)
    sample = sample[np.where(sample['MET']>35)]
    sample = sample[np.where(sample['Mt']>40)]
    sample = sample[np.where(sample['lep_iso']/sample['lep_Pt'] < 0.1)]
    sample = sample[np.where(sample['ph_istight']==0)]
    sample = sample[np.where(sample['ph_iso_cone40'] < 4)]
    return sample
def Inclusive_D(csvfile=default_csv):    
    sample = DefVars(csv_file = csvfile)
    sample = sample[np.where(sample['MET']>35)]
    sample = sample[np.where(sample['Mt']>40)]
    sample = sample[np.where(sample['lep_iso']/sample['lep_Pt'] < 0.1)]
    sample = sample[np.where(sample['ph_istight']==0)]
    sample = sample[np.where(sample['ph_iso_cone40'] > 6)]
    return sample
def Inclusive_Bprime(csvfile=default_csv):    
    sample = DefVars(csv_file = csvfile)
    sample = sample[np.where(sample['MET']>35)]
    sample = sample[np.where(sample['Mt']>40)]
    sample = sample[np.where(sample['lep_iso']/sample['lep_Pt'] > 0.1)]
    sample = sample[np.where(sample['ph_istight'])]
    sample = sample[np.where(sample['ph_iso_cone40'] < 4)]
    return sample
def Inclusive_Cprime(csvfile=default_csv): 
    sample = DefVars(csv_file = csvfile)
    sample = sample[np.where(sample['MET']<20)]
    sample = sample[np.where(sample['Mt']<20)]
    sample = sample[np.where(sample['lep_iso']/sample['lep_Pt'] < 0.1)]
    sample = sample[np.where(sample['ph_istight'])]
    sample = sample[np.where(sample['ph_iso_cone40'] < 4)]
    return sample
def Inclusive_Dprime(csv_file=default_csv): 
    sample = DefVars(csv_file = csvfile)
    sample = sample[np.where(sample['MET']<20)]
    sample = sample[np.where(sample['Mt']<20)]
    sample = sample[np.where(sample['lep_iso']/sample['lep_Pt'] > 0.1)]
    sample = sample[np.where(sample['ph_istight'])]
    sample = sample[np.where(sample['ph_iso_cone40'] < 4)]
    return sample
############################################################
#########define two jet region here ########################
############################################################
def TwoJet_sig(csvfile=default_csv):
    sample = Inclusive_sig(csvfile=csvfile)
    sample = sample[np.where(sample['njets']==2)]
    return sample
def TwoJet_B(csvfile=default_csv):
    sample = Inclusive_B(csvfile=csvfile)
    sample = sample[np.where(sample['njets']==2)]
    return sample
def TwoJet_C(csvfile=default_csv):
    sample = Inclusive_C(csvfile=csvfile)
    sample = sample[np.where(sample['njets']==2)]
    return sample
def TwoJet_D(csvfile=default_csv):
    sample = Inclusive_D(csvfile=csvfile)
    sample = sample[np.where(sample['njets']==2)]
    return sample
def TwoJet_Bprime(csvfile=default_csv):
    sample = Inclusive_Bprime(csvfile=csvfile)
    sample = sample[np.where(sample['njets']==2)]
    return sample
def TwoJet_Cprime(csvfile=default_csv):
    sample = Inclusive_Cprime(csvfile=csvfile)
    sample = sample[np.where(sample['njets']==2)]
    return sample
def TwoJet_Dprime(csvfile=default_csv):
    sample = Inclusive_Dprime(csvfile=csvfile)
    sample = sample[np.where(sample['njets']==2)]
    return sample
### calculate components function 05-28-2014, save events according to keys, define control region here instead of in SFrame
def CalComp(samples={'data':None,'wenugvbs':None,'wenug':None,'wenu':None,'zee':None,'dp':None,'ttbar':None},norms={'data':1,'wenugvbs':1,'wenug':1,'wenu':24769592/1.540386934e+15,'zee':1,'dp':1,'ttbar':1,'tg':1},CR={'nonIsoPhCut':6,'nonIsoElCut':0.1,'highMET':35,'highMt':40,'lowMET':20,'lowMt':20}):        
    if samples['data'] is None:
       print 'please provide inputs!'
    keys=['data','wenugvbs','wenug','wenu','zee','dp','ttbar','tg']
    #luminosity_rescale = 4.32
    luminosity_rescale = 1.
    components=dict((el,0) for el in keys)
    ph_cr=dict((el,0) for el in keys)
    el_cr=dict((el,0) for el in keys)    
    NA=dict((el,0) for el in keys)
    NB=dict((el,0) for el in keys)
    NC=dict((el,0) for el in keys)
    ND=dict((el,0) for el in keys)
    NBprime=dict((el,0) for el in keys)
    NCprime=dict((el,0) for el in keys)
    NDprime=dict((el,0) for el in keys)
    A=dict((el,0) for el in keys)
    B=dict((el,0) for el in keys)
    C=dict((el,0) for el in keys)
    D=dict((el,0) for el in keys)
    Bprime=dict((el,0) for el in keys)
    Cprime=dict((el,0) for el in keys)
    Dprime=dict((el,0) for el in keys)
    
    output=dict((el,0) for el in keys+['wenu_mc','dp_mc'])
    normalization = dict((el,0) for el in keys)
  
    ############################################################################################
    ##############################load numbers in different regions##############################
    #############################################################################################
    
    ## data,separate to four regions
    for key in keys:
        ##photon control region##
        ph_cr[key] = samples[key][np.where(samples[key]['MET']>CR['highMET'])]
        ph_cr[key] = ph_cr[key][np.where(ph_cr[key]['Mt']>CR['highMt'])]
        ph_cr[key] = ph_cr[key][np.where(ph_cr[key]['lep_iso']/ph_cr[key]['lep_Pt'] < 0.1)]
        ##electron control region ##    
        el_cr[key] = samples[key][np.where(samples[key]['ph_istight']==1)]
        el_cr[key] = el_cr[key][np.where(el_cr[key]['ph_iso_cone40'] < 4)]

        A[key] = ph_cr[key][np.where(ph_cr[key]['ph_istight']==1)]# signal region
        A[key] = A[key][np.where(A[key]['ph_iso_cone40'] < 4)]# Iso
        B[key] = ph_cr[key][np.where(ph_cr[key]['ph_istight']==1)] # tight photon
        B[key] = B[key][np.where(B[key]['ph_iso_cone40'] > CR['nonIsoPhCut'])]# nonIso
        C[key] = ph_cr[key][np.where(ph_cr[key]['ph_istight']==0)]# loose photon
        C[key] = C[key][np.where(C[key]['ph_iso_cone40'] < 4)] # Iso
        D[key] = ph_cr[key][np.where(ph_cr[key]['ph_istight']==0)] # loose photon
        D[key] = D[key][np.where(D[key]['ph_iso_cone40'] > CR['nonIsoPhCut'])] # dblRev 
        Bprime[key] = el_cr[key][np.where(el_cr[key]['lep_iso']/el_cr[key]['lep_Pt'] > CR['nonIsoElCut'])] # nonIso
        Bprime[key] = Bprime[key][np.where(Bprime[key]['MET']>CR['highMET'])] # high MET
        Bprime[key] = Bprime[key][np.where(Bprime[key]['Mt']>CR['highMt'])] # high transverse mass
        Cprime[key] = el_cr[key][np.where(el_cr[key]['lep_iso']/el_cr[key]['lep_Pt'] < 0.1)]
        Cprime[key] = Cprime[key][np.where(Cprime[key]['MET']<CR['lowMET'])] # low MET
        Cprime[key] = Cprime[key][np.where(Cprime[key]['Mt']<CR['lowMt'])] # low Mt
        Dprime[key] = el_cr[key][np.where(el_cr[key]['lep_iso']/el_cr[key]['lep_Pt'] > CR['nonIsoElCut'])] # nonIso
        Dprime[key] = Dprime[key][np.where(Dprime[key]['MET']<CR['lowMET'])] # low MET
        Dprime[key] = Dprime[key][np.where(Dprime[key]['Mt']<CR['lowMt'])] # low Mt

    A_dp_forsigleak = samples['dp'][np.where(samples['dp']['ph_istight']==1)]
    A_dp_forsigleak = A_dp_forsigleak[np.where(A_dp_forsigleak['ph_iso_cone40'] < 4)]
    A_dp_forsigleak = A_dp_forsigleak[np.where(A_dp_forsigleak['lep_iso']/A_dp_forsigleak['lep_Pt']<0.1)]
    B_dp_forsigleak = samples['dp'][np.where(samples['dp']['ph_istight']==1)]
    B_dp_forsigleak = B_dp_forsigleak[np.where(B_dp_forsigleak['ph_iso_cone40'] > CR['nonIsoPhCut'])]
    B_dp_forsigleak = B_dp_forsigleak[np.where(B_dp_forsigleak['lep_iso']/B_dp_forsigleak['lep_Pt']<0.1)]
    C_dp_forsigleak = samples['dp'][np.where(samples['dp']['ph_istight']==0)]
    C_dp_forsigleak = C_dp_forsigleak[np.where(C_dp_forsigleak['ph_iso_cone40'] < 4)]
    C_dp_forsigleak = C_dp_forsigleak[np.where(C_dp_forsigleak['lep_iso']/C_dp_forsigleak['lep_Pt']<0.1)]
    D_dp_forsigleak = samples['dp'][np.where(samples['dp']['ph_istight']==0)]
    D_dp_forsigleak = D_dp_forsigleak[np.where(D_dp_forsigleak['ph_iso_cone40'] > CR['nonIsoPhCut'])]
    D_dp_forsigleak = D_dp_forsigleak[np.where(D_dp_forsigleak['lep_iso']/D_dp_forsigleak['lep_Pt']<0.1)]
    NA_dp_forsigleak = ufloat(sum(A_dp_forsigleak['weight']/luminosity_rescale),sqrt(sum((A_dp_forsigleak['weight']/luminosity_rescale)**2)))
    NB_dp_forsigleak = ufloat(sum(B_dp_forsigleak['weight']/luminosity_rescale),sqrt(sum((B_dp_forsigleak['weight']/luminosity_rescale)**2)))
    NC_dp_forsigleak = ufloat(sum(C_dp_forsigleak['weight']/luminosity_rescale),sqrt(sum((C_dp_forsigleak['weight']/luminosity_rescale)**2)))
    ND_dp_forsigleak = ufloat(sum(D_dp_forsigleak['weight']/luminosity_rescale),sqrt(sum((D_dp_forsigleak['weight']/luminosity_rescale)**2)))
    print '#####################################'
    print 'NA_dp_forsigleak : ',NA_dp_forsigleak
    print 'NB_dp_forsigleak : ',NB_dp_forsigleak
    print 'NC_dp_forsigleak : ',NC_dp_forsigleak
    print 'ND_dp_forsigleak : ',ND_dp_forsigleak
    print '#####################################'
    
    # calculate number of events in each regions
    NA['data'] = ufloat(size(A['data']['weight']),sqrt(size(A['data']['weight'])))
    NB['data'] = ufloat(size(B['data']['weight']),sqrt(size(B['data']['weight'])))
    NC['data'] = ufloat(size(C['data']['weight']),sqrt(size(C['data']['weight'])))
    ND['data'] = ufloat(size(D['data']['weight']),sqrt(size(D['data']['weight'])))
    NBprime['data'] = ufloat(size(Bprime['data']['weight']),sqrt(size(Bprime['data']['weight'])))
    NCprime['data'] = ufloat(size(Cprime['data']['weight']),sqrt(size(Cprime['data']['weight'])))
    NDprime['data'] = ufloat(size(Dprime['data']['weight']),sqrt(size(Dprime['data']['weight'])))
    
    for key in keys[1:]:
        NA[key] = ufloat(sum(A[key]['weight']*A[key]['mc_event_weight']*norms[key]/luminosity_rescale),sqrt(sum((A[key]['weight']*A[key]['mc_event_weight']*norms[key]/luminosity_rescale)**2)))
        NB[key] = ufloat(sum(B[key]['weight']*B[key]['mc_event_weight']*norms[key]/luminosity_rescale),sqrt(sum((B[key]['weight']*B[key]['mc_event_weight']*norms[key]/luminosity_rescale)**2)))
        NC[key] = ufloat(sum(C[key]['weight']*C[key]['mc_event_weight']*norms[key]/luminosity_rescale),sqrt(sum((C[key]['weight']*C[key]['mc_event_weight']*norms[key]/luminosity_rescale)**2)))
        ND[key] = ufloat(sum(D[key]['weight']*D[key]['mc_event_weight']*norms[key]/luminosity_rescale),sqrt(sum((D[key]['weight']*D[key]['mc_event_weight']*norms[key]/luminosity_rescale)**2)))
        NBprime[key] = ufloat(sum(Bprime[key]['weight']*Bprime[key]['mc_event_weight']*norms[key]/luminosity_rescale),sqrt(sum((Bprime[key]['weight']*Bprime[key]['mc_event_weight']*norms[key]/luminosity_rescale)**2)))
        NCprime[key] = ufloat(sum(Cprime[key]['weight']*Cprime[key]['mc_event_weight']*norms[key]/luminosity_rescale),sqrt(sum((Cprime[key]['weight']*Cprime[key]['mc_event_weight']*norms[key]/luminosity_rescale)**2)))
        NDprime[key] = ufloat(sum(Dprime[key]['weight']*Dprime[key]['mc_event_weight']*norms[key]/luminosity_rescale),sqrt(sum((Dprime[key]['weight']*Dprime[key]['mc_event_weight']*norms[key]/luminosity_rescale)**2)))
    
    #############################################################################################
    ##################################calculate photon fakes###################################
    #############################################################################################
    NA_ewk=NA['ttbar']+NA['zee']+NA['wenu']
    #############################################################################################
    ##################################calculate electron fakes###################################
    #############################################################################################
    R_dp=1
    #R_dp=NA['wenu']*ND['wenu']/(NC['wenu']*NB['wenu'])
    ###formulas to calculate photon jet normalization
    NBprime_ewk=NBprime['ttbar']+NBprime['zee']+NBprime['wenu']
    NCprime_ewk=NCprime['ttbar']+NCprime['zee']+NCprime['wenu']
    NDprime_ewk=NDprime['ttbar']+NDprime['zee']+NDprime['wenu']
    #C_Bprime=(NBprime['wenug']+NBprime['wenu'])/(NA['wenug']+NA['wenu'])
    #C_Cprime=(NCprime['wenug']+NCprime['wenu'])/(NA['wenug']+NA['wenu'])
    #C_Dprime=(NDprime['wenug']+NDprime['wenu'])/(NA['wenug']+NA['wenu'])
    C_Bprime=NBprime['wenug']/NA['wenug']
    C_Cprime=NCprime['wenug']/NA['wenug']
    C_Dprime=NDprime['wenug']/NA['wenug']    

    Eprime=NDprime['data']-NDprime_ewk+(NA['data']-NA_ewk)*C_Dprime-R_dp*(NBprime['data']-NBprime_ewk)*C_Cprime-(NCprime['data']-NCprime_ewk)*C_Bprime*R_dp
    Fprime=4*(C_Bprime*C_Cprime*R_dp-C_Dprime)*((NA['data']-NA_ewk)*(NDprime['data']-NDprime_ewk)-(NCprime['data']-NCprime_ewk)*(NBprime['data']-NBprime_ewk)*R_dp)/(Eprime*Eprime)
    Gprime=2*(C_Bprime*C_Cprime*R_dp-C_Dprime)
    NA_dp_DD = NA['data']-NA_ewk-Eprime*(-1+sqrt(1+Fprime))/Gprime
    #NA_wenu_DD = NA_wjets-NA_dp_DD

    print '                                                                                                          '
    print '####################################  jet->el Closure test  ##############################################'
    print '                                                                                                          '

    print 'dp MC: '
    print 'NA                                                 : ','{:.2f}'.format(NA['dp'])
    print "NB'                                                : ",'{:.2f}'.format(NBprime['dp'])
    print "NC'                                                : ",'{:.2f}'.format(NCprime['dp'])
    print "ND'                                                : ",'{:.2f}'.format(NDprime['dp'])
    print "R'                                                 : ",'{:.4f}'.format(NA['dp']*NDprime['dp']/(NCprime['dp']*NBprime['dp']))
    print 'Signal leakge :'
    print 'C_Bprime=(NBprime_wg)/(NA_wg) : ','{:.4f}'.format(C_Bprime)
    print 'C_Cprime=(NCprime_wg)/(NA_wg) : ','{:.4f}'.format(C_Cprime)
    print 'C_Dprime=(NDprime_wg)/(NA_wg) : ','{:.4f}'.format(C_Dprime)
    print '                                                                                                          '
    print '##################################  γ+jets DD estimation  ################################################'
    print '                                                                                                          '
    print 'Eprime = NDprime_data-NDprime_ewk+(NA_data-NA_ewk)*C_Dprime'
    print '         -R_dp*(NBprime_data-NBprime_ewk)*C_Cprime'
    print '         -(NCprime_data-NCprime_ewk)*C_Bprime*R_dp'
    print 'Fprime = (4/Eprime^2)*(C_Bprime*C_Cprime*R_dp-C_Dprime)*'
    print '         ((NA_data-NA_ewk)*(NDprime_data-NDprime_ewk)-  '
    print '         (NCprime_data-NCprime_ewk)*(NBprime_data-NBprime_ewk)*R_dp)'
    print 'Gprime = 2*(C_Bprime*C_Cprime*R_dp-C_Dprime) '
    print '                                                                                                          '
    print 'Eprime                                                      : ','{:.4f}'.format(Eprime)
    print 'Fprime                                                      : ','{:.4f}'.format(Fprime)
    print 'Gprime                                                      : ','{:.4f}'.format(Gprime)
    print 'Eprime*(-1+sqrt(1+Fprime))/Gprime                           : ','{:.4f}'.format(Eprime*(-1+sqrt(1+Fprime))/Gprime)
    print 'NA_dp_DD : NA_data-NA_ewk-Eprime*(-1+sqrt(1+Fprime))/Gprime : ','{:.4f}'.format(NA_dp_DD)
    #print 'Scale in signal region A                                    : ','{:.4f}'.format(NA_dp_DD/NBprime['dp'])
    print '                                                                                                          '
#    NA_ewk=NA['ttbar']+NA['zee']+NA_dp_DD
#    NB_ewk=NB['ttbar']+NB['zee']+NB['dp']
#    NC_ewk=NC['ttbar']+NC['zee']+NC['dp']
#    ND_ewk=ND['ttbar']+ND['zee']+ND['dp']
    ### not considering dp contributions, consider it to be signal
    NA_ewk=NA['ttbar']+NA['zee']
    NB_ewk=NB['ttbar']+NB['zee']
    NC_ewk=NC['ttbar']+NC['zee']
    ND_ewk=ND['ttbar']+ND['zee']
    C_B=(NB['wenug'])/(NA['wenug'])
    C_C=(NC['wenug'])/(NA['wenug'])
    C_D=(ND['wenug'])/(NA['wenug'])
#    C_B=(NB['wenug']+NB['dp'])/(NA['wenug']+NA['dp'])
#    C_C=(NC['wenug']+NC['dp'])/(NA['wenug']+NA['dp'])
#    C_D=(ND['wenug']+ND['dp'])/(NA['wenug']+NA['dp'])
#    C_B = 1/2*(NB['wenug']/NA['wenug']+NB_dp_forsigleak/NA_dp_forsigleak)
#    C_C = 1/2*(NC['wenug']/NA['wenug']+NC_dp_forsigleak/NA_dp_forsigleak)
#    C_D = 1/2*(ND['wenug']/NA['wenug']+ND_dp_forsigleak/NA_dp_forsigleak)
#    C_B = (NB['wenug']+NB_dp_forsigleak)/(NA['wenug']+NA_dp_forsigleak)
#    C_C = (NC['wenug']+NC_dp_forsigleak)/(NA['wenug']+NA_dp_forsigleak)
#    C_D = (ND['wenug']+ND_dp_forsigleak)/(NA['wenug']+NA_dp_forsigleak)
    #C_D = (ND['wenug']+ND_dp_forsigleak)/(NA['wenug']+NA_dp_forsigleak)
    print 'NB_dp_forsigleak/NA_dp_forsigleak',NB_dp_forsigleak/NA_dp_forsigleak
    print 'NC_dp_forsigleak/NA_dp_forsigleak',NC_dp_forsigleak/NA_dp_forsigleak
    print 'ND_dp_forsigleak/NA_dp_forsigleak',ND_dp_forsigleak/NA_dp_forsigleak
    print 'NB_dp/NA_dp',NB['dp']/NA['dp']
    print 'NC_dp/NA_dp',NC['dp']/NA['dp']
    print 'ND_dp/NA_dp',ND['dp']/NA['dp']

    Rmc = 1
    #Rmc = NA['wenu']*ND['wenu']/(NC['wenu']*NB['wenu'])
    K = NA['data']-NA_ewk
    E = ND['data'] - ND_ewk+(NA['data']-NA_ewk)*C_D-(NB['data']-NB_ewk)*C_C*Rmc-(NC['data']-NC_ewk)*C_B*Rmc
    F = 4*(C_B*C_C*Rmc-C_D)*((NA['data']-NA_ewk)*(ND['data']-ND_ewk)-(NC['data']-NC_ewk)*(NB['data']-NB_ewk)*Rmc)/(E*E)
    G = 2*(C_B*C_C*Rmc-C_D)
    NA_wjets = K-E*(-1+sqrt(1+F))/G
    NA_wenu_DD = NA_wjets 
    print '##########################################################################################################'
    print '###################################  Begin analysis ######################################################'
    print '##########################################################################################################'
    print '                                                                                                          '
    print '################################      jet->γ Closure test      ############################################'
    print '                                                                                                          '
    print 'wenu MC :'
    print 'NA                               : ','{:.2f}'.format(NA['wenu'])
    print 'NB                               : ','{:.2f}'.format(NB['wenu'])
    print 'NC                               : ','{:.2f}'.format(NC['wenu'])
    print 'ND                               : ','{:.2f}'.format(ND['wenu'])
    print 'R: NA*ND/(NB*NC)                 : ','{:.4f}'.format(NA['wenu']*ND['wenu']/(NC['wenu']*NB['wenu']))
    print 'Signal leakge :   '
    print 'C_B=(NB_wg)/(NA_wg)  :','{:.4f}'.format(C_B)
    print 'C_C=(NC_wg)/(NA_wg)  :','{:.4f}'.format(C_C)
    print 'C_D=(ND_wg)/(NA_wg)  :','{:.4f}'.format(C_D)
    print '                                                                                                          '
    print '##############################   wjets DD estimation     ################################################'
    print '                                                                                                          '
    print 'K = NA_data-NA_ewk                                                                                    :','{:.4f}'.format(K)
    print 'E = ND_data - ND_ewk+(NA_data-NA_ewk)*C_D-(NB_data-NB_ewk)*C_C*Rmc-(NC_data-NC_ewk)*C_B*Rmc           :','{:.4f}'.format(E)
    print 'F = 4*(C_B*C_C*Rmc-C_D)*((NA_data-NA_ewk)*(ND_data-ND_ewk)-(NC_data-NC_ewk)*(NB_data-NB_ewk)*Rmc)/E^2 :','{:.4f}'.format(F)
    print 'G = 2*(C_B*C_C*Rmc-C_D)                                                                               :','{:.4f}'.format(G)
    print 'E*(-1+sqrt(1+F))/G                                                                                    :','{:.4f}'.format(E*(-1+sqrt(1+F))/G)
    print 'NA_wjets = K-E*(-1+sqrt(1+F))/G                                                                       :','{:.4f}'.format(NA_wjets)

    print '###################################################################################################'
    print '##################################    Summary  ####################################################'
    print '###################################################################################################'
    print '                                                                                                          '
    print 'Signal and background components: '
    print "Sample & NA & NB & NC & ND & NB' &NC' & ND'"
    for key in keys:
        print key,' & ','{:.2f}'.format(NA[key]),'&','{:.4f}'.format(NB[key]),'&','{:.4f}'.format(NC[key]),'&','{:.4f}'.format(ND[key]),'&','{:.4f}'.format(NBprime[key]),'&','{:.4f}'.format(NCprime[key]),'&','{:.4f}'.format(NDprime[key])
    for key in keys:
        print key,' & $','{:L}'.format(NA[key]),'$&$','{:L}'.format(NB[key]),'$&$','{:L}'.format(NC[key]),'$&$','{:L}'.format(ND[key]),'$&$','{:L}'.format(NBprime[key]),'$&$','{:L}'.format(NCprime[key]),'$&$','{:L}'.format(NDprime[key]),'$',r'\\'
    print 'wenu DD &','{:.4f}'.format(NA_wenu_DD),', wenu MC : ','{:.4f}'.format(NA['wenu'])
    print 'dp DD &','{:.4f}'.format(NA_dp_DD),', dp MC : ','{:.4f}'.format(NA['dp'])
    #components['Rprime'] = NA['dp']*NDprime['dp']/(NCprime['dp']*NBprime['dp'])
    #components['R'] = NA['wenu']*ND['wenu']/(NC['wenu']*NB['wenu'])
    components['C_B'] = C_B
    components['C_C'] = C_C
    components['C_D'] = C_D
    components['C_Bprime'] = C_Bprime
    components['C_Cprime'] = C_Cprime
    components['C_Dprime'] = C_Dprime
    components['data']=NA['data']
    components['wenug']=NA['wenug']
    components['wenugvbs']=NA['wenugvbs']
    components['dp_DD']=NA_dp_DD
    components['wenu_DD']=NA_wenu_DD
    components['zee']=NA['zee']
    components['ttbar']=NA['ttbar']
    components['wenu']=NA['wenu']
    components['dp']=NA['dp']
    components['tg']=NA['tg']
    components['signalyield'] = NA['data']-NA_dp_DD-NA_wenu_DD-NA['zee']-NA['ttbar']-NA['tg']
    output['data'] = A['data']
    normalization['data'] = 1

    for key in keys+['wenu_mc','dp_mc']:
        if key in ['wenugvbs','zee','ttbar','wenug','tg']:
           output[key] = A[key]
           normalization[key] = 1
        if key is 'dp':
           output[key] = Bprime['data']
           normalization[key] = (NBprime['data'])/components['dp_DD']
        if key is 'wenu':
           output[key] = D['data']
           normalization[key] = (ND['data'])/components['wenu_DD']
        if key is 'wenu_mc':
           output[key] = A['wenu']
           normalization[key] = 1
        if key is 'dp_mc':    
           output[key] = A['dp']
           normalization[key] = 1
    print 'Signal yield from Data : ', NA['data']-NA_dp_DD-NA_wenu_DD-NA['zee']-NA['ttbar']-NA['tg']
    return components,output,normalization  

def apply_vbs_cuts(sample=DefVars(csv_file=default_csv),LeadingJetPt=30,SubleadingJetPt=30,MjjCut=600,dYjjCut=2,PtBalanceCut=.1):
    highMjj = sample[np.where(sample['Mjj']>MjjCut)]
    highdYjj = highMjj[np.where(abs(highMjj['dYjj']) > dYjjCut)]
    highdYjj = highdYjj[np.where(abs(highdYjj['pt_balance']) < PtBalanceCut)]
    #highdYjj = highdYjj[np.where(abs(highdYjj['dYj0_lg']) > 1)]
    highdYjj = highdYjj[np.where(highdYjj['bveto70']==0)]
    highdYjj = highdYjj[np.where(highdYjj['jet_leading_Pt']>LeadingJetPt)]
    highdYjj = highdYjj[np.where(highdYjj['jet_subleading_Pt']>SubleadingJetPt)]
    #highdYjj = highdYjj[np.where(highdYjj['Mjj']<3000)]
    #highdYjj = highdYjj[np.where(abs(highdYjj['lg_Centrality'])<0.6)]
    return highdYjj
# define wgqcd control region
def wgqcd_control_cuts(sample=DefVars(csv_file=default_csv),LeadingJetPt=30,SubleadingJetPt=30,MjjCut=600,dYjjCut=2,PtBalanceCut=.1):
    highMjj = sample[np.where(sample['Mjj']>MjjCut)]
    highdYjj = highMjj[np.where(abs(highMjj['dYjj']) > dYjjCut)]
    highdYjj = highdYjj[np.where(abs(highdYjj['pt_balance']) > PtBalanceCut)]
    highdYjj = highdYjj[np.where(highdYjj['bveto70']==0)]
    highdYjj = highdYjj[np.where(highdYjj['jet_leading_Pt']>LeadingJetPt)]
    highdYjj = highdYjj[np.where(highdYjj['jet_subleading_Pt']>SubleadingJetPt)]
    return highdYjj
### some plot utilities
def plot(x,y,*args,**kwargs):
    nominal_curve = pyplot.plot(x, unumpy.nominal_values(y), *args, **kwargs)
    pyplot.fill_between(x, 
                        unumpy.nominal_values(y)-unumpy.std_devs(y), 
                        unumpy.nominal_values(y)+unumpy.std_devs(y),
                        facecolor=nominal_curve[0].get_color(),
                        edgecolor='face',
                        alpha=0.1,
                        linewidth=0)
    return nominal_curve
def errorplot(x,y,*args,**kwargs):
    nominal_curve = errorbar(x, unumpy.nominal_values(y),unumpy.std_devs(y), *args, **kwargs)
    return nominal_curve


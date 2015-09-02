# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>
# <codecell>
from uncertainties import *
from uncertainties.umath import *
import numpy as np
cpool = [ '#bd2309', '#bbb12d', '#1480fa', '#14fa2f', '#000000',
              '#faf214', '#2edfea', '#ea2ec4', '#ea2e40', '#cdcdcd',
              '#577a4d', '#2e46c0', '#f59422', '#219774', '#8086d9']
# <codecell>
def LoadData(csv_base='/Users/Mia/Documents/WgZgPhysics/Analysis/WgTemplates/0521_2014/',bkgtype='default',
             sample=['data'],process=['data'],loadedsample={'data':None},njets=0,Mjj=0,dYjj=0,dYj0_lg=999,pt_balance=0):
    print '###################################################################################################'
    print 'Loading csv files from '+csv_base
    print 'Cuts applied: njets>= ',njets,',Mjj >= ',Mjj,'GeV',',dYjj>= ',dYjj,'dYj0_lg',dYj0_lg,'pt_balance',pt_balance
    variables = ['RunNumber','EventNumber','njets','lumi_weight','pileup_weight','bveto70','bveto80','bveto85',
                 'bvetotruth','fsr_veto','el_region','ph_region','truthregion','averageIntPerXing','jet_leading_E',
                 'jet_leading_Pt','jet_leading_Eta','jet_leading_Phi','jet_subleading_E','jet_subleading_Pt',
                 'jet_subleading_Eta','jet_subleading_Phi','lep_Charge','lep_E','lep_Pt','lep_Eta','lep_Phi','lep_sf',
                 'lep_iso','ph_E','ph_Pt','ph_Eta','ph_Phi','ph_istight','ph_iso_cone20','ph_iso_cone30','ph_iso_cone40',
                 'ph_pdgId','ph_mother','METx','METy','MET','Mt','Mlg','Ptlg','dRlg','dRlj0','dRlj1','dYgj0','dYgj1',
                 'dRgj0','dRgj1','Mjj','Ptjj','dYjj','dRjj','Mlgj0','Mlgj1','Ptlgj0','Ptlgj1','Mlgjj','Ptlgjj',
                 'dYj0_lg','dYj1_lg','pt_balance','pt_balance_noMET','lg_Centrality','l_Centrality','weight']
    i = 0
    for f in process:
        #print 'loading file : ',sample[i]
        dp = np.genfromtxt(csv_base+sample[i]+'.csv', delimiter=',', skip_header=10,
                     skip_footer=10, names=variables)
        data = dp
        #data = dp[np.where(dp['ph_Pt']>40)]
        data = data[np.where(data['dRlg']>0.4)]
        #data = data[np.where(data['Mlg']<75)]
        #data = data[np.where(data['Mlg']>105)]

        if f is 'wenu':
           data=data[np.where(data['fsr_veto']==0)]
        if 'gjet' in bkgtype: 
            data=data[np.where(data['el_region']==0)]
        if 'ejet' in bkgtype: 
            data=data[np.where(data['ph_region']==0)]
        data=data[np.where(data['njets']>=njets)]
        #data=data[np.where(data['Mjj']>=Mjj)]
        #data=data[np.where(data['dYjj']>=dYjj)]
        #data=data[np.where(data['dYj0_lg']<=dYj0_lg)]ds
        #data=data[np.where(data['pt_balance']>=pt_balance)]
        loadedsample[f]=data
        #loadedsample[sample[i]]=data
        i = i+1        
    return loadedsample
       # print samples['data']['MET']

# <codecell>
### calculate components function 05-28-2014, save events according to keys, define control region here instead of in SFrame
def CalComp(samples={'data':None,'wenugvbs':None,'wenug':None,'wenu':None,'zee':None,'dp':None,'ttbar':None}):        
    if samples['data'] is None:
       print 'please provide inputs!'
    #print np.where(samples['data']['el_region']==0)
    keys=['data','wenugvbs','wenug','wenu','zee','dp','ttbar']
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
    
    ############################################################################################
    ##############################load numbers in different regions##############################
    #############################################################################################
    ## data
    for key in keys:
        ph_cr[key] = samples[key][np.where(samples[key]['el_region']==0)]
        el_cr[key] = samples[key][np.where(samples[key]['ph_region']==0)]
        A[key] = ph_cr[key][np.where(ph_cr[key]['ph_region']==0)]# signal region
        B[key] = ph_cr[key][np.where(ph_cr[key]['ph_istight']==1)] # tight photon
        B[key] = B[key][np.where(B[key]['ph_iso_cone40'] > 6)]# nonIso
        C[key] = ph_cr[key][np.where(ph_cr[key]['ph_istight']==0)]# loose photon
        C[key] = C[key][np.where(C[key]['ph_iso_cone40'] < 4)] # Iso
        D[key] = ph_cr[key][np.where(ph_cr[key]['ph_istight']==0)] # loose photon
        D[key] = D[key][np.where(D[key]['ph_iso_cone40'] > 6)] # dblRev 
        Bprime[key] = el_cr[key][np.where(el_cr[key]['lep_iso']/el_cr[key]['lep_Pt'] > 0.1)] # nonIso
        Bprime[key] = Bprime[key][np.where(Bprime[key]['MET']>35)] # high MET
        Bprime[key] = Bprime[key][np.where(Bprime[key]['Mt']>40)] # high transverse mass
        Cprime[key] = el_cr[key][np.where(el_cr[key]['lep_iso']/el_cr[key]['lep_Pt'] < 0.1)]
        Cprime[key] = Cprime[key][np.where(Cprime[key]['MET']<20)] # low MET
        Cprime[key] = Cprime[key][np.where(Cprime[key]['Mt']<20)] # low Mt
        Dprime[key] = el_cr[key][np.where(el_cr[key]['lep_iso']/el_cr[key]['lep_Pt'] > 0.1)] # nonIso
        Dprime[key] = Dprime[key][np.where(Dprime[key]['MET']<20)] # low MET
        Dprime[key] = Dprime[key][np.where(Dprime[key]['Mt']<20)] # low Mt
    NA['data'] = ufloat(np.size(A['data']['weight']),sqrt(np.size(A['data']['weight'])))
    NB['data'] = ufloat(np.size(B['data']['weight']),sqrt(np.size(B['data']['weight'])))
    NC['data'] = ufloat(np.size(C['data']['weight']),sqrt(np.size(C['data']['weight'])))
    ND['data'] = ufloat(np.size(D['data']['weight']),sqrt(np.size(D['data']['weight'])))
    NBprime['data'] = ufloat(np.size(Bprime['data']['weight']),sqrt(np.size(Bprime['data']['weight'])))
    NCprime['data'] = ufloat(np.size(Cprime['data']['weight']),sqrt(np.size(Cprime['data']['weight'])))
    NDprime['data'] = ufloat(np.size(Dprime['data']['weight']),sqrt(np.size(Dprime['data']['weight'])))
 
    for key in keys[1:]:
        NA[key] = ufloat(np.sum(A[key]['weight']),sqrt(np.sum(A[key]['weight']*A[key]['weight'])))
        NB[key] = ufloat(np.sum(B[key]['weight']),sqrt(np.sum(B[key]['weight']*B[key]['weight'])))
        NC[key] = ufloat(np.sum(C[key]['weight']),sqrt(np.sum(C[key]['weight']*C[key]['weight'])))
        ND[key] = ufloat(np.sum(D[key]['weight']),sqrt(np.sum(D[key]['weight']*D[key]['weight'])))
        NBprime[key] = ufloat(np.sum(Bprime[key]['weight']),sqrt(np.sum(Bprime[key]['weight'])))
        NCprime[key] = ufloat(np.sum(Cprime[key]['weight']),sqrt(np.sum(Cprime[key]['weight'])))
        NDprime[key] = ufloat(np.sum(Dprime[key]['weight']),sqrt(np.sum(Dprime[key]['weight'])))
    #############################################################################################
    ##################################calculate photon fakes###################################
    #############################################################################################
    NA_ewk=NA['ttbar']+NA['zee']
    NB_ewk=NA['ttbar']+NB['zee']
    NC_ewk=NC['ttbar']+NC['zee']
    ND_ewk=ND['ttbar']+ND['zee']
    C_B=(NB['wenug']+NB['dp'])/(NA['wenug']+NA['dp'])
    C_C=(NC['wenug']+NC['dp'])/(NA['wenug']+NA['dp'])
    C_D=(ND['wenug']+ND['dp'])/(NA['wenug']+NA['dp'])
    Rmc = 1
    K = NA['data']-NA_ewk
    E = ND['data'] - ND_ewk+(NA['data']-NA_ewk)*C_D-(NB['data']-NB_ewk)*C_C*Rmc-(NC['data']-NC_ewk)*C_B*Rmc
    F = 4*(C_B*C_C*Rmc-C_D)*((NA['data']-NA_ewk)*(ND['data']-ND_ewk)-(NC['data']-NC_ewk)*(NB['data']-NB_ewk)*Rmc)/(E*E)
    G = 2*(C_B*C_C*Rmc-C_D)
    NA_wjets = K-E*(-1+sqrt(1+F))/G
    NA_wenu_DD = NA_wjets
    print '                                                                                                          '
    print '################################      Closure test      #################################################'
    print '                                                                                                          '
    print 'wenu MC :'
    print 'NA                               : ','{:.2f}'.format(NA['wenu'])
    print 'NB                               : ','{:.2f}'.format(NB['wenu'])
    print 'NC                               : ','{:.2f}'.format(NC['wenu'])
    print 'ND                               : ','{:.2f}'.format(ND['wenu'])
    print 'R: NA*ND/(NB*NC)                 : ','{:.4f}'.format(NA['wenu']*ND['wenu']/(NC['wenu']*NB['wenu']))
    print 'Signal leakge :   '
    print 'C_B=(NB_wg+NB_dp)/(NA_wg+NA_dp)  :','{:.4f}'.format(C_B)
    print 'C_C=(NC_wg+NC_dp)/(NA_wg+NA_dp)  :','{:.4f}'.format(C_C)
    print 'C_D=(ND_wg+ND_dp)/(NA_wg+NA_dp)  :','{:.4f}'.format(C_D)
    print '                                                                                                          '
    print '##############################   wjets DD estimation     ################################################'
    print '                                                                                                          '
    print 'K = NA_data-NA_ewk                                                                                    :','{:.4f}'.format(K)
    print 'E = ND_data - ND_ewk+(NA_data-NA_ewk)*C_D-(NB_data-NB_ewk)*C_C*Rmc-(NC_data-NC_ewk)*C_B*Rmc           :','{:.4f}'.format(E)
    print 'F = 4*(C_B*C_C*Rmc-C_D)*((NA_data-NA_ewk)*(ND_data-ND_ewk)-(NC_data-NC_ewk)*(NB_data-NB_ewk)*Rmc)/E^2 :','{:.4f}'.format(F)
    print 'G = 2*(C_B*C_C*Rmc-C_D)                                                                               :','{:.4f}'.format(G)
    print 'E*(-1+sqrt(1+F))/G                                                                                    :','{:.4f}'.format(E*(-1+sqrt(1+F))/G)
    print 'NA_wjets = K-E*(-1+sqrt(1+F))/G                                                                       :','{:.4f}'.format(NA_wjets)

    #############################################################################################
    ##################################calculate electron fakes###################################
    #############################################################################################
    R_dp=1
    ###formulas to calculate photon jet normalization
    NBprime_ewk=NBprime['ttbar']#+NDprime_zee
    NCprime_ewk=NCprime['ttbar']#+NBprime_zee
    NDprime_ewk=NDprime['ttbar']#+NCprime_zee
    C_Bprime=(NBprime['wenug']+NBprime['wenu'])/(NA['wenug']+NA['wenu'])
    C_Cprime=(NCprime['wenug']+NBprime['wenu'])/(NA['wenug']+NA['wenu'])
    C_Dprime=(NDprime['wenug']+NDprime['wenu'])/(NA['wenug']+NA['wenu'])

    Eprime=NDprime['data']-NDprime_ewk+(NA['data']-NA_ewk)*C_Dprime-R_dp*(NBprime['data']-NBprime_ewk)*C_Cprime-(NCprime['data']-NCprime_ewk)*C_Bprime*R_dp
    Fprime=4*(C_Bprime*C_Cprime*R_dp-C_Dprime)*((NA['data']-NA_ewk)*(NDprime['data']-NDprime_ewk)-(NCprime['data']-NCprime_ewk)*(NBprime['data']-NBprime_ewk)*R_dp)/(Eprime*Eprime)
    Gprime=2*(C_Bprime*C_Cprime*R_dp-C_Dprime)
    NA_dp_DD = NA['data']-NA_ewk-Eprime*(-1+sqrt(1+Fprime))/Gprime
    print '                                                                                                          '
    print '####################################  Closure test  ######################################################'
    print '                                                                                                          '

    print 'dp MC: '
    print 'NA                                                 : ','{:.2f}'.format(NA['dp'])
    print "NB'                                                : ",'{:.2f}'.format(NBprime['dp'])
    print "NC'                                                : ",'{:.2f}'.format(NCprime['dp'])
    print "ND'                                                : ",'{:.2f}'.format(NDprime['dp'])
    print "R'                                                 : ",'{:.4f}'.format(NA['dp']*NDprime['dp']/(NCprime['dp']*NBprime['dp']))
    print 'Signal leakge :'
    print 'C_Bprime=(NBprime_wg+NBprime_wenu)/(NA_wg+NA_wenu) : ','{:.4f}'.format(C_Bprime)
    print 'C_Cprime=(NCprime_wg+NCprime_wenu)/(NA_wg+NA_wenu) : ','{:.4f}'.format(C_Cprime)
    print 'C_Dprime=(NDprime_wg+NDprime_wenu)/(NA_wg+NA_wenu) : ','{:.4f}'.format(C_Dprime)
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
    print 'Scale in signal region A                                    : ','{:.4f}'.format(NA_dp_DD/(NBprime['dp']+NCprime['dp']+NDprime['dp']))
    print '                                                                                                          '
    print '###################################################################################################'
    print '##################################    Summary  ####################################################'
    print '###################################################################################################'
    print '                                                                                                          '
    print 'Signal and background components: '
    print "Sample & NA & NB & NC & ND & NB' &NC' & ND'"
    for key in keys:
        print key,' : ','{:.2f}'.format(NA[key]),'&','{:.4f}'.format(NB[key]),'&','{:.4f}'.format(NC[key]),'&','{:.4f}'.format(ND[key]),'&','{:.4f}'.format(NBprime[key]),'&','{:.4f}'.format(NCprime[key]),'&','{:.4f}'.format(NDprime[key])
    print 'wenu DD :','{:.4f}'.format(NA_wenu_DD),', wenu MC : ','{:.4f}'.format(NA['wenu'])
    print 'dp DD :','{:.4f}'.format(NA_dp_DD),', dp MC : ','{:.4f}'.format(NA['dp'])
    components['data']=NA['data']
    components['wenug']=NA['wenug']
    components['wenugvbs']=NA['wenugvbs']
    components['dp']=NA_dp_DD
    components['wenu']=NA_wenu_DD
    components['zee']=NA['zee']
    components['ttbar']=NA['ttbar']
    
    return components
## variables should be the same for all files (unless there are changes in the branches)
postfix = {'data':'PeriodB','wenugvbs':'sherpa','wenug':'sherpa','wenu':'sherpa','zee':'alpgen','dp':'','ttbar':'mcnlo'}
process =['data','wenugvbs','wenug','wenu','zee','dp','ttbar']
loadedsample = dict((el,0) for el in process) 
samples = []
#append postfix to the process to create a list of sample names
for f in process:
    if f is 'dp': filename = f
    else:filename = f+'_'+postfix[f]
    samples.append(filename)
print 'Going to use these samples:'
print samples    
loadedsample = dict((el,0) for el in samples)
loadedsample = LoadData(csv_base='/Users/Mia/Documents/WgZgPhysics/Analysis/WgTemplates/0528_2014_Medium/',
                     bkgtype='non',sample=samples,loadedsample=loadedsample,process=process,njets=0,Mjj=0,dYjj=2.4)
TightPlusPlus_comp=CalComp(samples=loadedsample)
print TightPlusPlus_comp
        


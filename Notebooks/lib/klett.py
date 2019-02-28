def Klett81b(r,P, k=1.,n=1,sf0=None,Rm=None):
    import numpy as np
    import copy 
    import pylab
    #print np.shape(P)
    #print np.shape(r)
    S=np.log(P*r**2)
    pix = np.where(P <=0)
    if Rm == None:
        Rm = np.size(S)-2 
        if np.size(pix) == 1:
            Rm = pix[0]-2
        elif np.size(pix) > 1:
            Rm = pix[0][0]-2
        
    #print "eeeS",S[0]   
    nbins = np.size(S)
    dr = (r[1]-r[0])
    s = np.zeros(shape=[nbins]) #Extinction coef.
    '''
    def sm_fun(cc):
    
        Rb=nbins-5-cc   
        Rm=nbins-1-cc   
        Sb = np.nanmean(S[nbins-5-cc])
        Sm = np.nanmean(S[nbins-1-cc])
        #print Sb,Sm
    
        inte0 = 0
        
        for R_ in range(Rb,Rm):
            inte0 = np.nansum([inte0,2*np.exp((S[R_]-Sm)/k)*dr/k])
            #print inte0
        
        sf=(np.exp((Sb-Sm)/k)-1)/inte0 
        return [sf,Rm,Sm]
    
    for cc0 in range(100):
        sf0,Rm,Sm = sm_fun(cc0)
        if sf0 > 0:
            break
#        if sf0 < 0:
#            break
    '''
    #Rm = nbins-cc0-1
    s[Rm] = sf0[Rm]         
    Sm = S[Rm] 
    
    print "sm : ", sf0[Rm],"Rm=",Rm, Sm  
    
        
    for j in range(n):
        for i in range(Rm+1):
                
            RtoRm = range(i,Rm+1)
            
            inte = 0
            
            for R in RtoRm:
                inte = np.nansum([inte,2*np.exp((S[R]-Sm)/k)*dr/k])
                #inte = np.nansum([inte,(2/k)*(np.sign(P[R]/P[-1])*(abs((r[R]**2)*P[R]/((r[-1]**2)*P[-1])))**(1/k))*dr])
                #print inte,S[R],Sm
            s[i] = np.exp((S[i]-Sm)/k)/(s[Rm]**-1+inte)        
    s = np.ma.masked_where(s<=0, s)                    
    return s


def Klett81f(r,P, k=1.,n=1,sf0=None,R0=None):
    import numpy as np
    import copy 
    import pylab
    #print np.shape(P)
    #print np.shape(r)
    S=np.log(P*r**2)
    pix = np.where(P <=0)
    Rm = np.size(S)-2 
    if np.size(pix) == 1:
        Rm = pix[0]-2
    elif np.size(pix) > 1:
        Rm = pix[0][0]-2
        
    #print "eeeS",S[0]   
    nbins = np.size(S)
    dr = (r[1]-r[0])
    s = np.zeros(shape=[nbins]) #Extinction coef.

    #Rm = nbins-cc0-1
    s[R0] = sf0[R0]         
    S0 = S[R0] 
    
    print "sm : ", sf0[R0],"Rm=",R0, S0  
    
        
    for j in range(n):
        for i in range(R0,Rm+1):
                
            R0toR = range(R0,i)
            
            inte = 0
            
            for R in R0toR:
                inte = np.nansum([inte,2*np.exp((S[R]-S0)/k)*dr/k])
                #inte = np.nansum([inte,(2/k)*(np.sign(P[R]/P[-1])*(abs((r[R]**2)*P[R]/((r[-1]**2)*P[-1])))**(1/k))*dr])
                #print inte,S[R],Sm
            s[i] = np.exp((S[i]-S0)/k)/(s[R0]**-1-inte)        
    s = np.ma.masked_where(s<=0, s)                    
    return s

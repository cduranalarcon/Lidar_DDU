def Klett81b2(r,P, k=0.1,n=2,sf0=None,Rm=None):
    #Version revised on Feb. 27th 2019
    import numpy as np
    
    S=np.log(P)
    nbins = np.size(S)
    dr = (r[1]-r[0])
    s = np.zeros(shape=[nbins]) #Extinction coef.
    Rm = nbins-1
    s[Rm] = sf0[Rm]         
    Sm = S[Rm] 
        
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
    
    return s, Rm
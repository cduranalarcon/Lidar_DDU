# Last version 03102019, mod: limite to while iteration

def DP_simp(r,AA0,nstd,sm = 5):
    import pandas as pd
    import numpy as np
    from running_mean import running_mean 
    
    AA=running_mean(AA0,sm)#[sm-1:]
    rr=r[(sm-1)/2:-(sm-1)/2]#pd.rolling_mean(r,sm)[sm-1:]

    Er = AA - AA0[(sm-1)/2:-(sm-1)/2]#[sm-1:]
    n = np.arange(0,np.size(AA))
    flag = np.zeros(shape = np.size(AA))
    flag[0] = 1
    flag[-1] = 1
    flag2 = np.zeros(shape = np.size(AA))
    flag2[0] = 1
    flag2[-1] = 1

    end = False
    nlevels = 0
    while end == False:
        
        nlevels = nlevels + 1
        
        if nlevels > np.size(r)*2: end = True 
        
        pix = np.squeeze(np.where(flag2 == 1))

        p1 = AA[pix[0]]
        p2 = AA[pix[1]]
        n1 = n[pix[0]]
        n2 = n[pix[1]]

        L = ((p2-p1)/(n2-n1))*(n-n1)+p1

        d = abs(AA-L)
        d[0:n1+1] = 0
        d[n2:] = 0
        d[np.where(AA < 0)] = 0
        eps_mean = np.nanmean(Er[n1:n2+1])
        eps_std = nstd*np.nanstd(Er[n1:n2+1])
        eps = eps_mean + eps_std

        if ((np.size(d)>1) & (np.max(d) > 0)):
            nm = np.where(d == np.max(d))
            dm = d[nm]

            if dm > eps: 
                #print dm, eps, eps_mean,eps_std , nm
                flag[nm] = 1
                flag2[nm] = 1
            else:
                #print "menor que el umbral"
                for i in range(n1,n2):
                    flag2[i] = 1

                for i in range(np.size(flag)-1):
                    if ((flag2[i] == 1) & (flag2[i+1]== 1)):
                        flag2[i] = 2
                        #print "1"
        else:
            for i in range(np.size(flag)-1):
                if ((flag2[i] == 1) & (flag2[i+1]== 1)):
                    flag2[i] = 2
            #print "terminado"
        if flag2[-2] == 2: end = True  
    return [rr[np.squeeze(np.where(flag == 1))], AA[np.squeeze(np.where(flag == 1))],rr,AA]            
#print nm,dm,eps,np.squeeze(np.where(flag2 == 1))  
#pylab.plot(n,AA)
#pylab.scatter(n[np.squeeze(np.where(flag == 1))],AA[np.squeeze(np.where(flag == 1))])
#print flag2 
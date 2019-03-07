def BG_corr(P,r,year,month,day, rcf0 = 9, pol = 'parallel',color = "blue"):
    
    import sys, os
    sys.path.append("lib")
    from Sigma_mol import sigma_mol
    from scipy.interpolate import interp1d      
    import time
    from calendar import timegm
    import pylab
    import numpy as np
    from scipy import stats

    utc_time = time.strptime(str(year)+"-"+str(month).zfill(2)+"-"+str(day).zfill(2)+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    epoch_time = timegm(utc_time)  
    
    month2 = time.gmtime(epoch_time+3600*24)[1]
    day2 = time.gmtime(epoch_time+3600*24)[2]
    
    [sigma1, h1] = sigma_mol(year = year, month = month, day = day)
    [sigma2, h2] = sigma_mol(year = year, month = month2, day = day2)
    

    if (np.size(sigma1) > 1) & (np.size(sigma2) > 1):
        mat = np.ma.masked_where(np.array([sigma1.filled(-9999),sigma2.filled(-9999)]) == -9999,np.array([sigma1.filled(-9999),sigma2.filled(-9999)]))
        sigma = np.nanmean(mat,axis = 0)[10:]/100000. #transfor cm-1 to km-1  
        h = h1[10:]

    if (np.size(sigma1) == 1) & (np.size(sigma2) > 1):
        sigma = sigma2[10:]/100000. #transfor cm-1 to km-1 
        h = h2[10:]

    if (np.size(sigma1) > 1) & (np.size(sigma2) == 1):
        sigma = sigma1[10:]/100000. #transfor cm-1 to km-1 
        h = h1[10:]
        
    rcf = np.squeeze(np.where(h < rcf0))[-1] 
    rcf_lidar = np.squeeze(np.where(r >= rcf0))[0]
    
    Tm = np.exp((-2*np.cumsum(sigma[rcf:])*(h[1]-h[0])))
    Tm_rcf = np.exp((-2*np.cumsum(sigma[0:rcf])*(h[1]-h[0])))
    Tm_full = np.exp((-2*np.cumsum(sigma)*(h[1]-h[0])))    
    
    if pol == 'parallel':
        beta = 0.996*sigma/((8*np.pi/3)*1.0401)
    if pol == 'perpendicular': 
        beta = 0.00366*sigma/((8*np.pi/3)*1.0401)
        
    f = interp1d(h[rcf:], Tm*beta[rcf:]/(h[rcf:]**2))    
        
    lm = stats.linregress(x = f(r[rcf_lidar:]), y = P[rcf_lidar:])
    
    #pylab.plot(f(r[rcf_lidar:]),P[rcf_lidar:], "o", color = color)
    
    #pylab.plot(np.linspace(np.min(f(r[rcf_lidar:])),np.max(f(r[rcf_lidar:])),3), np.linspace(np.min(f(r[rcf_lidar:])),np.max(f(r[rcf_lidar:])),3)*lm[0]+lm[1], color = color, label = str(year)+"/"+str(month).zfill(2)+"/"+str(day).zfill(2) + " ("+r'$y = $'+str(int(lm[0]))+r'$x$ + ' + str(round(lm[1],2))+", "+r'$r^2 = $'+str(round(lm[2],2))+")")
    
    #print np.mean(P[rcf_lidar:])
    #ax.ticklabel_format(axis = "x", style='scientific',scilimits = (-1,2))
    
    #pylab.legend(frameon = False, loc = "upper left" , fontsize = 18)
    
    return [lm,Tm_full,h,sigma]

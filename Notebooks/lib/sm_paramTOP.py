def sm_paramTOP(year = None, month = None, day = None, UTC = "00", epoch_time  = None , tstamp_fmt = "%Y-%m-%d %H:%M:%S", path_rs = "C:/Users/duran/Documents/PhD/DDU/DATA/Soundings-DATA/DDU/"):
    import time
    import numpy as np
    from scipy.optimize import curve_fit
    
    if epoch_time != None:
        times = time.gmtime(epoch_time)
        year = times[0]
        month = times[1]
        day = times[2]
    
    try:
        file_rs = path_rs+"DDU_RS_"+str(year)+str(month).zfill(2)+str(day).zfill(2)+"_"+UTC+".txt"
        
        txt = open(file_rs,"r")
        
        h_rs = []
        T_rs = []
        P_rs = []

        for l in txt:
            h0 = l.split("\t")[0]
            P0 = l.split("\t")[1]
            T0 = l.split("\t")[2]
            if h0 != "NaN":
                if float(h0)/1000. >=10: break
                if float(h0)/1000. <=9: continue

                h_rs.append(float(h0)/1000.)
            else:
                h_rs.append(-9999.)
            if P0 != "NaN":
                P_rs.append(float(P0))
            else:
                P_rs.append(-9999.)
            if T0 != "NaN":
                T_rs.append(float(T0))
            else:
                T_rs.append(-9999.)

        h_rs = np.array(h_rs)
        P_rs = np.array(P_rs)
        T_rs = np.array(T_rs)

        h_rs = np.ma.masked_where(h_rs == -9999,h_rs)
        P_rs = np.ma.masked_where(P_rs == -9999,P_rs)
        T_rs = np.ma.masked_where(T_rs == -9999,T_rs)

        NA = 6.02214e23 # mol-1
        Ra = 8.314472 # J K-1 mol-1 
        Qs = 5.167e-27 #cm2

        sigma_rs= NA*Qs*P_rs/(T_rs*Ra)
        
        def func2(x,A,B):
            import numpy as np
            return  (A*np.exp(B*x))

        if np.sum(sigma_rs.mask == False) > 5:
            params, pcov = curve_fit(func2, h_rs[sigma_rs.mask == False], sigma_rs[sigma_rs.mask == False])#,bounds=(0, [9999999999., np.mean(y_per)]))

            return params  
        else:
            return np.array([-9999.,-9999.])  
    except:
        return np.array([-9999.,-9999.])  
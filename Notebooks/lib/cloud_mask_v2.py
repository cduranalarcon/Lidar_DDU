def cloud_mask2(PPP,r,doPlot = False, th = 3, nstd=3, sm = 5, check = False, check2 = False):
    import pylab
    from DP_simp import DP_simp
    from copy import copy
    #import simplification, pylab, sys
    #from simplification import cutil
    import numpy as np
    #sys.path.append("lib")
    #from lidar_integrating_space_time import Lidar_space_time as lidar_integ
    #import pandas as pd

    #SimCoords = cutil.simplify_coords
    #SimCoords_vw = cutil.simplify_coords_vw
    
    #coords = []
    #sm = 5
    #R = pd.rolling_mean(r[3:],sm)
    #PR2 = pd.rolling_mean(((P[3:]-bgc)*((r[3:]/1000.)**2)*O),sm)
    #for i in range(np.size(O[sm-1:])):
    #    coords.append([r[3:][sm-1:][i]/1000.,PR2[sm-1:][i]])
    #coords = np.array(coords)    

    #DP = SimCoords(coords, 0.5)
    X,Y,R,PR2 = DP_simp(r,PPP,nstd,sm)
    #X = DP[1:,0]
    #Y = DP[1:,1]        
    #pylab.scatter(X,Y,color = 'black',facecolors='white',s=50)#none')

    npoints = np.size(X)
    
    #mat2 = lidar_integ(date = "2017.02.26", space = 1, timee = 15)  
    #r0 = mat2[3] + mat2[3][0]  
    #P0 = mat2[0][4*12,:]
    #cs_slope = -61.26692217560352 #-25

    slope2 = []
    slope = []
    for i in range(1,npoints):
        s = (Y[i]-Y[i-1])/(X[i]-X[i-1])
        s2 = (np.log(Y[i]/Y[i-1]))/(X[i]-X[i-1])
        slope.append(s)
        slope2.append(s2)
    X2 = X[:]
    Y2 = Y[:]
    base = []
    top = []
    peak = []
    selected_b = False
    peak0 = -999999.
    selected_b = False
    possible_t = False
    clearsky_slope = copy(slope)
    clearsky_slope = np.array(clearsky_slope)
    #print X2
    #print Y2
    
    for i in range(1,npoints-1):
        if check == True: print i,X2[i-1],Y2[i-1],slope[i-1],slope2[i-1],(slope2[i-1] > -0.5) & (slope2[i-1] < 0) 
        if ((slope[i-1] > 0) & (selected_b == False)):
            if check2 == True: print "stop1"
            #print i,X2[i-1],Y2[i-1],slope[i],"Base"
            selected_b = True
            base.append([X2[i-1],Y2[i-1]])
            PbRb2 = Y2[i-1]
        #print selected_b     
        if  selected_b == True:
            if peak0 < Y2[i-1]:
                peak0x = X2[i-1]
                peak0 =  Y2[i-1]
                if check2 == True: print "stop2",i, base,"/",peak,"/",top
                #print "size base ", np.size(base)
                #tabback 
            if (slope2[i-1] > -0.5) & (slope2[i-1] < 0) & (Y2[i-1] > PbRb2) & (np.size(base) == 2) & (X2[i-1] <= 1):
                #base = []
                peak = []
                top = []
                peak0 = -999999.
                #selected_b = False    
                possible_t = False
                #print "elimiado"
                if check2 == True: print "stop3",i, base,"/",peak,"/",top
                continue
                #stop
            csky = clearsky_slope[:i]

            cskypix = np.squeeze(np.where(csky != -9999.))

            if np.size(cskypix)>= 10 :
                cs_slope = np.nanmean(csky[cskypix][-10:-1])
                #print "slope",csky[cskypix][-10:-1]
                condSlope = slope[i-1] > cs_slope
            elif i < 10: 
                #print i,"/", csky,"/", cskypix,"/",np.size(csky)
                if np.size(cskypix) > 1 : 
                    cs_slope = np.nanmean(csky[cskypix][:-1])
                else:
                    cs_slope = np.nanmean(csky[cskypix])

                    condSlope = slope[i-1] > cs_slope
                #tabback 
                #if np.size(cskypix) == 0 :
                    #cs_slope = 
            condSlope = (slope2[i-1] > -0.5) & (slope2[i-1] < 0) 
                #    stop
                    #print "slope",csky[cskypix]
                #print csky, cs_slope
            #cs_slope = -200
            
            #print Y2[i],Y2[i+1],(Y2[i+1] <= PbRb2), PbRb2,(i == npoints-2) ,(slope[i] < 0)
            #sttop
            #print "check2"
            if ((slope[i-1] < 0) & (condSlope) & (Y2[i-1] <= PbRb2)):
                if check2 == True: print "stop4", base,"/",peak,"/",top
                #stop
                #print "hea"
                #print i,X2[i-1],Y2[i-1],slope[i],"Top"
                top.append([X2[i-1],Y2[i-1]])
                peak.append([peak0x,peak0])
                peak0 = -999999.
                selected_b = False
                possible_t = False 
            elif ((slope[i-1] < 0) & (Y2[i] <= PbRb2) & (i == npoints-2)):
                if check2 == True: print "stop5", base,"/",peak,"/",top
                top.append([X2[i],Y2[i]])
                peak.append([peak0x,peak0])
                peak0 = -999999.
                selected_b = False
                possible_t = False  
            elif  ((slope[i] < 0) & (Y2[i+1] <= PbRb2) & (i == npoints-2)):
                if check2 == True: print "stop6", base,"/",peak,"/",top
                if peak0 < Y2[i]:
                    peak0x = X2[i]
                    peak0 =  Y2[i]
                top.append([X2[i+1],Y2[i+1]])
                peak.append([peak0x,peak0])
                peak0 = -999999.
                selected_b = False
                possible_t = False   
              
            elif ((slope[i-1] < 0) & (i == npoints-2)):
                if check2 == True: print "stop7", base,"/",peak,"/",top
                top.append([X2[i],Y2[i]])
                peak.append([peak0x,peak0])
                peak0 = -999999.
                selected_b = False
                possible_t = False  
            elif  ((slope[i] < 0) & (i == npoints-2)):
                if check2 == True: print "stop8", base,"/",peak,"/",top
                if peak0 < Y2[i]:
                    peak0x = X2[i]
                    peak0 =  Y2[i]
                top.append([X2[i+1],Y2[i+1]])
                peak.append([peak0x,peak0])
                peak0 = -999999.
                selected_b = False
                possible_t = False   
            elif  ((slope[i] < 0) & (i == npoints-1)):
                if check2 == True: print "stop11", base,"/",peak,"/",top
                if peak0 < Y2[i]:
                    peak0x = X2[i]
                    peak0 =  Y2[i]
                top.append([X2[i+1],Y2[i+1]])
                peak.append([peak0x,peak0])
                peak0 = -999999.
                selected_b = False
                possible_t = False        
        
        if ((slope[i-1] > 0) & (selected_b == False)):
            if check2 == True: print "stop9", base,"/",peak,"/",top
            #print i,X2[i-1],Y2[i-1],slope[i],"Top"
            selected_b = True
            base.append([X[i-1],Y[i-1]])
            PbRb2 = Y[i-1]
            #print cs_slope
        if (selected_b == True): 
            if check2 == True: print "stop10", base,"/",peak,"/",top
            clearsky_slope[i] = -9999.
            #clearsky_slope = np.ma.masked_where(clearsky_slope == -9999.,clearsky_slope) 
    top = np.array(top) 
    peak = np.array(peak)  
    
    if np.size(top)>1:
        base = np.array(base)[0:np.shape(top)[0],:] 
   
    clearsky_slope = np.ma.masked_where(np.array(clearsky_slope) == -9999.,np.array(clearsky_slope)) 
    #pylab.scatter(X,Y,color = 'black',facecolors='white',s=50)#none')

    if doPlot == True:  
        pylab.plot(r,PPP,":", color = "black",zorder=0)
        pylab.plot(R,PR2, color = "black",zorder=0)
        pylab.xlabel("Height [km a.g.l.]")
        pylab.ylabel("R-corrected signal [a.u.]") 
        pylab.scatter(X,Y,color = 'black',facecolors='white',s=50)#none')
        
    if np.size(top)>1:
        PeakToBase = peak[:,1]/base[:,1]

        top_Pr2 = np.ma.masked_where(PeakToBase < th,top[:,1])
        peak_Pr2 = np.ma.masked_where(PeakToBase < th,peak[:,1])
        base_Pr2 = np.ma.masked_where(PeakToBase < th,base[:,1])
        top_r = np.ma.masked_where(PeakToBase < th,top[:,0])
        peak_r = np.ma.masked_where(PeakToBase < th,peak[:,0])
        base_r = np.ma.masked_where(PeakToBase < th,base[:,0])

        if doPlot == True:

            #pylab.plot(r0[700:]/1000.,P0[700:]*((r0[700:]/1000.)**2), color = "gray",zorder=0)
            #pylab.yscale("log")
            pylab.scatter(base_r,base_Pr2,color = 'red',facecolors='white',s=100)#none')
            pylab.scatter(peak_r,peak_Pr2,color = 'blue',facecolors='white',s=100)#none')
            pylab.scatter(top_r,top_Pr2,color = 'green',facecolors='white',s=100)#none')     

        B = base_r[np.where(PeakToBase > th)].data
        T = top_r[np.where(PeakToBase > th)].data

        r_mask = np.zeros(shape = np.shape(r)) 

        mMPix = []

        for i in range(np.size(B)):
            pix = np.where((r >= B[i]) & (r <= T[i]))
            mMPix.append([min(pix[0]),max(pix[0])])
            r_mask[pix] = 1
        mMPix = np.array(mMPix)    

        nl = 0

        layers  = []
        layers_mask  = []

        for i in range(1,np.size(r_mask)-1):
            if ((r_mask[i] == r_mask[i-1]) & (r_mask[i] != r_mask[i+1])):
                if nl == 0:
                    layers.append([0,i])
                    layers_mask.append(r_mask[i])
                    nl = nl+1
                else:
                    layers.append([layers[-1][1],i])
                    layers_mask.append(r_mask[i])
                    nl = nl+1

        layers = np.array(layers)
        layers_mask = np.array(layers_mask)    
        mat = [r_mask, B, T,layers,layers_mask]
        #print mat[2],"t1"
    else:
        
        mat = [-9999, -9999, -9999,-9999,-9999]
    #print mat[2],"t2"    
    return mat #,slope, X, Y,mMPix]
    #return [base[:,0],top[:,0],peak[:,1]/base[:,1]]
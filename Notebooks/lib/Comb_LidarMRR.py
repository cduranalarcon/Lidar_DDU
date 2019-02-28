def Comb_LidarMRR(layers_mask, Par90_bgc, r,nstd,sm, Ze, hours):
    from DP_simp import DP_simp
    import numpy as np
    from copy import copy
    from time2epoch import time2epoch
    import pylab
    
    layers_mask2 = copy(layers_mask)
    for h in range(np.shape(Par90_bgc)[0]):###############################################
        try:
            time_lidar = time2epoch(year = year, month = month, day = day, hour = int((h)/6.),minute=int(round(60*((h)/6. - int((h)/6.)))))
            pix_time = np.squeeze(np.where(time_lidar == times_MRR))
            pixmask = np.squeeze(np.where(layers_mask[h,15:].mask == True))[2]
            if (Ze[pix_time,1] > -18) & (layers_mask[h,18] == 1):    

                #pylab.plot(Height_MRR,Ze[pix_time,:])
                #pylab.plot(R,Y2)

                #print Height_MRR[1]
                #from DP_simp import DP_simp

                #pixmask = np.squeeze(np.where(layers_mask[h,15:].mask == True))[2]

                X,Y,R_,PR2 = DP_simp(r[15:][0:pixmask],Par90_bgc[h,18:][0:pixmask],nstd,sm)    

                #pylab.plot(X,Y,"o")

                slope3 = []
                for i in range(1,np.size(X[:])):
                    s3 = (np.log(Y[i]/Y[i-1]))/(X[i]-X[i-1])
                    slope3.append(s3)
                #pylab.plot(X[0:-1],slope3,'o-')
                #pylab.axis([0.,7,-1,1])

                base2 = []
                top2 = []

                base2 = X[0]
                Ybase2 = Y[0]

                #print 0, X[0],slope3[i],(slope3[i] <= 0) & (slope3[0] > -0.5)
                for i in range(1,np.size(X)):
                    notfound  = False
                    #print i
                    pix = np.where(r <= X[i])    
                    if (2 in layers_mask[h,:][pix]):
                        if np.size(np.squeeze(np.where(layers_mask[h,:][pix] == 2)))>1:
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,:][pix] == 2))[0]]
                        else:
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,:][pix] == 2))]
                        #print "break2"
                        break
                    notfound  = True           

                #stop    
                count = 0

                if notfound  == True: 
                    for i in range(1,np.size(slope3)):
                        #top2 = X[i] 
                        notfound  = False
                        #print i, X[i],slope3[i],(slope3[i] <= 0) & (slope3[i] > -0.5)
                        if ((slope3[i] <= 0) & (slope3[i] > -0.5) & (Y[i]< Ybase2)):
                            top2 = X[i]
                            #print "break1"
                            count = count+1
                            if (count == 2): break
                        else:
                            count = 0
                        notfound  = True

                if notfound  == True:    
                    for i in range(i,np.size(X)):
                        notfound  = False
                        #print i
                        pix = np.where(r <= X[i])    
                        if (1 in layers_mask[h,:][pix]):
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,:][pix] == 1))[-1]]
                            #print "break3"
                            break
                        notfound  = True    

                #print str(int((h)/6.)).zfill(2)+":"+str(int(round(60*((h)/6. - int((h)/6.))))).zfill(2), '; Base =',base2, '. Top =',top2

                pixfin = np.squeeze(np.where((r >= base2) & (r <= top2) & (layers_mask.mask[h,:] != True)))
                layers_mask2[h,:][pixfin] = 3
        except:
            check= h
        
    return layers_mask2

def Comb_LidarMRR2(layers_mask, Par90_bgc, r,nstd,sm, Ze, hours):
    from DP_simp import DP_simp
    import numpy as np
    from copy import copy
    from time2epoch import time2epoch
    import pylab
    print r[15]
    layers_mask2 = copy(layers_mask)
    for h in range(np.shape(Par90_bgc)[0]):###############################################
        try:
            time_lidar = time2epoch(year = year, month = month, day = day, hour = int((h)/6.),minute=int(round(60*((h)/6. - int((h)/6.)))))
            pix_time = np.squeeze(np.where(time_lidar == times_MRR))
            pixmask = np.squeeze(np.where(layers_mask[h,15:].mask == True))[2]
            if (Ze[pix_time,1] > -18) & (layers_mask[h,18] == 1):    

                #pylab.plot(Height_MRR,Ze[pix_time,:])
                #pylab.plot(R,Y2)

                #print Height_MRR[1]
                #from DP_simp import DP_simp

                #pixmask = np.squeeze(np.where(layers_mask[h,15:].mask == True))[2]

                X,Y,R_,PR2 = DP_simp(r[15:][0:pixmask],Par90_bgc[h,15:][0:pixmask],nstd,sm)    

                #pylab.plot(X,Y,"o")

                slope3 = []
                for i in range(1,np.size(X[:])):
                    s3 = (np.log(Y[i]/Y[i-1]))/(X[i]-X[i-1])
                    slope3.append(s3)
                #pylab.plot(X[0:-1],slope3,'o-')
                #pylab.axis([0.,7,-1,1])

                base2 = []
                top2 = []

                base2 = X[0]
                Ybase2 = Y[0]

                #print 0, X[0],slope3[i],(slope3[i] <= 0) & (slope3[0] > -0.5)
                for i in range(1,np.size(X)):
                    notfound  = False
                    #print i
                    pix = np.where(r <= X[i])    
                    if (2 in layers_mask[h,:][pix]):
                        if np.size(np.squeeze(np.where(layers_mask[h,:][pix] == 2)))>1:
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,:][pix] == 2))[0]]
                        else:
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,:][pix] == 2))]
                        #print "break2"
                        break
                    notfound  = True           

                #stop    
                count = 0

                if notfound  == True: 
                    for i in range(1,np.size(slope3)):
                        #top2 = X[i] 
                        notfound  = False
                        #print i, X[i],slope3[i],(slope3[i] <= 0) & (slope3[i] > -0.5)
                        if ((slope3[i] <= 0) & (slope3[i] > -0.5) & (Y[i]< Ybase2)):
                            top2 = X[i]
                            #print "break1"
                            count = count+1
                            if (count == 2): break
                        else:
                            count = 0
                        notfound  = True

                if notfound  == True:    
                    for i in range(i,np.size(X)):
                        notfound  = False
                        #print i
                        pix = np.where(r <= X[i])    
                        if (1 in layers_mask[h,:][pix]):
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,:][pix] == 1))[-1]]
                            #print "break3"
                            break
                        notfound  = True    

                #print str(int((h)/6.)).zfill(2)+":"+str(int(round(60*((h)/6. - int((h)/6.))))).zfill(2), '; Base =',base2, '. Top =',top2

                pixfin = np.squeeze(np.where((r >= base2) & (r <= top2) & (layers_mask.mask[h,:] != True)))
                layers_mask2[h,:][pixfin] = 3
        except:
            check= h
        
    return layers_mask2

def Comb_LidarMRR3(layers_mask, Par90_bgc, r,nstd,sm,times_MRR, Ze, year, month, day,hours):
    from DP_simp import DP_simp
    import numpy as np
    from copy import copy
    from time2epoch import time2epoch
    import pylab
    #print np.shape(layers_mask), np.shape(Par90_bgc), np.shape(r), np.shape(nstd), np.shape(sm), np.shape(Ze), np.shape(hours)
    layers_mask2 = copy(layers_mask)
    
    for h in range(np.size(hours)):###############################################
        try:
        #if 1 == 1:
            time_lidar = time2epoch(year = year, month = month, day = day, hour = int((h)/6.),minute=int(round(60*((h)/6. - int((h)/6.)))))
            pix_time = np.squeeze(np.where(time_lidar == times_MRR))
            pixmask = np.squeeze(np.where(layers_mask[h,15:].mask == True))[2]
            #print layers_mask[h,15],layers_mask[h,16],layers_mask[h,17],layers_mask[h,18]
            #print np.uint64(Ze[pix_time,1] > -18),np.uint64(layers_mask[h,16] == 1)  
            if (np.uint64(Ze[pix_time,1] > -18) & np.uint64(layers_mask[h,16] == 1)):    
            #if ((Ze[pix_time,1] > -18) & (layers_mask[h,16] == 1)):        
                #print "ddd"
                #pylab.plot(Height_MRR,Ze[pix_time,:])
                #pylab.plot(R,Y2)

                #print Height_MRR[1]
                #from DP_simp import DP_simp

                #pixmask = np.squeeze(np.where(layers_mask[h,15:].mask == True))[2]

                X,Y,R_,PR2 = DP_simp(r[0:pixmask],Par90_bgc[h,:][0:pixmask],nstd,sm)    

                #pylab.plot(X,Y,"o")

                slope3 = []
                for i in range(1,np.size(X[:])):
                    s3 = (np.log(Y[i]/Y[i-1]))/(X[i]-X[i-1])
                    slope3.append(s3)
                #pylab.plot(X[0:-1],slope3,'o-')
                #pylab.axis([0.,7,-1,1])

                base2 = []
                top2 = []

                base2 = X[0]
                Ybase2 = Y[0]

                #print 0, X[0],slope3[i],(slope3[i] <= 0) & (slope3[0] > -0.5)
                for i in range(1,np.size(X)):
                    notfound  = False
                    #print i
                    pix = np.where(r <= X[i])    
                    if (2 in layers_mask[h,15:][pix]):
                        if np.size(np.squeeze(np.where(layers_mask[h,15:][pix] == 2)))>1:
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,15:][pix] == 2))[0]]
                        else:
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,15:][pix] == 2))]
                        #print "break2"
                        break
                    notfound  = True           

                #stop    
                count = 0

                if notfound  == True: 
                    for i in range(1,np.size(slope3)):
                        #top2 = X[i] 
                        notfound  = False
                        #print i, X[i],slope3[i],(slope3[i] <= 0) & (slope3[i] > -0.5)
                        if ((slope3[i] <= 0) & (slope3[i] > -0.5) & (Y[i]< Ybase2)):
                            top2 = X[i]
                            #print "break1"
                            count = count+1
                            if (count == 2): break
                        else:
                            count = 0
                        notfound  = True

                if notfound  == True:    
                    for i in range(i,np.size(X)):
                        notfound  = False
                        #print i
                        pix = np.where(r <= X[i])    
                        if (1 in layers_mask[h,15:][pix]):
                            top2 = r[pix][np.squeeze(np.where(layers_mask[h,15:][pix] == 1))[-1]]
                            #print "break3"
                            break
                        notfound  = True    

                #print str(int((h)/6.)).zfill(2)+":"+str(int(round(60*((h)/6. - int((h)/6.))))).zfill(2), '; Base =',base2, '. Top =',top2

                pixfin = np.squeeze(np.where((r >= base2) & (r <= top2) & (layers_mask.mask[h,15:] != True)))
                layers_mask2[h,15:][pixfin] = 3
        except:
            check = h
        
    return layers_mask2
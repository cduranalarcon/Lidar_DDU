# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:30:00 2018

@author: Claudio Duran-Alarcon
"""
import time, os, glob, pylab
from calendar import timegm
import numpy as np

t0=time.time() 

def Lidar_space_time(date = "2017.02.04",space = 13, timee = 60):

    #####################
    #To modify by the user
    #date = "2017.02.25" #Date YYYY.MM.DD
    #path = "C:/Users/lteadmin/Desktop/MCS6A Data/" #Check that the input path is OK
    #path = "I:/lidardata/MCS6A Data/"
    path = "C:/Users/admduaan/Documents/PhD/DDU/DATA/LIDAR/"
    #path_out = "C:/temp/lidar/" # modified if you want to change the output directory
    tr = timee #60 # Temporal aggregation [minutes] you can try with 10, 30, 60min for example
    #####################
    
    #outputs: plots of lidar signal, dep. ratio and mean number of acquisitions per minute.
    
        
    font = {'family'    :   'serif',
            'weight'    :   'normal',
            'size'      :   20}
    
    pylab.rc('font', **font)        
    
    def read_lidarfile(filename):
        import numpy as np
        f = open(filename,'r')
        data0 = np.array(f.readlines())
        f.close()    
        data_Size = np.size(data0)
      
        if (data_Size == 7883):      
            TDAT0 = np.array(data0[9:2633],dtype=float)#90% parallel
            TDAT1 = np.array(data0[2634:5258],dtype=float)#10% parallel
            TDAT2 = np.array(data0[5259:7883],dtype=float)#Perpendicular                
                         
            #simple background correction  
            #print "A", np.nanmean(TDAT1[(1300):])   
            
            #TDAT0 = np.array(TDAT0)-np.nanmean(TDAT0[(2624-150):]) #2624-150
            #TDAT1 = np.array(TDAT1)-np.nanmean(TDAT1[(2624-150):])   
            #TDAT2 = np.array(TDAT2)-np.nanmean(TDAT2[(2624-150):])
            #print np.shape(TDAT0)
            #print np.nanpercentile(TDAT1[(1300):],1)
            #print "B", np.nanmean(TDAT0[(2624-150):])   
            return [TDAT0[1:],TDAT1[1:],TDAT2[1:]]
    TZoff = 1 #Time Zone offset original data is in UTC+1 [h] do not change for DDU
    
    nt = 1440/tr+1 #number of steps
    
    mat_90par = np.zeros(shape=(nt,2623))
    mat_10par = np.zeros(shape=(nt,2623))
    mat_per = np.zeros(shape=(nt,2623))
    mat_npix= np.zeros(shape=(nt))
    
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    
    #path=path+year+"/"
    
    utc_ti = time.strptime(year+"-"+month+"-"+day+"T00:00:00", "%Y-%m-%dT%H:%M:%S")
    ti = timegm(utc_ti)
    tf = ti + 3600*24
    
    times = np.linspace(ti,tf,nt)
    
    year2 = str(time.gmtime(ti+3600*24)[0])
    month2 = str(time.gmtime(ti+3600*24)[1]).zfill(2)
    day2 = str(time.gmtime(ti+3600*24)[2]).zfill(2)
    
    path1 = path+year+"."+month+"."+day+"/MCS6A data/"
    times1 = []
    path2 = path+year2+"."+month2+"."+day2+"/MCS6A data/"
    times2 = []
    
    print "Reading data..."
    print "(It can takes a few minutes)"
    
    if os.path.exists(path1):
        os.chdir(path1)
        filenames1 = glob.glob("*.txt")
        for txt in filenames1:
            times1.append(timegm(time.strptime(txt[0:4]+"-"+txt[4:6]+"-"+txt[6:8] + "T"+txt[9:11]+":"+txt[12:14]+":"+txt[15:17], "%Y-%m-%dT%H:%M:%S")))
        times1=np.array(times1)-TZoff*3600    
        filenames1=np.array(filenames1)
        t_count = 0
        for t in times:
            if t < min(times1)-60*tr:
                t_count = t_count + 1    
                continue
            if t > max(times1)+60*tr:
                break
            pix = np.where((times1 <= t) & (times1 > t-60*tr))  
            npix = 0. 
            if np.size(pix) > 0 : 
                par90sum =np.zeros(shape = (2623))
                par10sum =np.zeros(shape = (2623))
                persum =np.zeros(shape = (2623))
                try:
                    
                    for ppix in pix[0]:
                        filename = path1+filenames1[ppix]  
                        
                        par90,par10,per = read_lidarfile(filename)
                        par90sum = par90sum + par90
                        par10sum = par10sum + par10
                        persum = persum + per
                        npix = npix+1. 
                except:
                    print "Problem reading the file " +filenames1[ppix]
                            
            if npix > 0:
                mat_90par[t_count,:] = par90sum/npix         
                mat_10par[t_count,:] = par10sum/npix         
                mat_per[t_count,:] = persum/npix   
                mat_npix[t_count] = npix    
    #        print t_count  
            t_count = t_count + 1
      
                 
    if os.path.exists(path2):
        os.chdir(path2)
        filenames2 = glob.glob("*.txt")
        for txt in filenames2:
            times2.append(timegm(time.strptime(txt[0:4]+"-"+txt[4:6]+"-"+txt[6:8] + "T"+txt[9:11]+":"+txt[12:14]+":"+txt[15:17], "%Y-%m-%dT%H:%M:%S")))
        times2=np.array(times2)-TZoff*3600    
        filenames2=np.array(filenames2)
        t_count = 0
        for t in times:
            try: 
                if t < min(times2)-60*tr:
                    t_count = t_count + 1    
                    continue
                if t > max(times2)+60*tr:
                    break
            except:
                1==1
    
            pix = np.where((times2 <= t) & (times2 > t-60*tr))
            npix = 0. 
            if np.size(pix) > 0 : 
                par90sum =np.zeros(shape = (2623))
                par10sum =np.zeros(shape = (2623))
                persum =np.zeros(shape = (2623))
                try:            
                    for ppix in pix[0]:
                        filename = path2+filenames2[ppix]
                        par90,par10,per = read_lidarfile(filename)
                        par90sum = par90sum + par90
                        par10sum = par10sum + par10
                        persum = persum + per
                        npix = npix+1. 
                except:
                    print "Problem reading the file " +filenames2[ppix]
                    
            if npix > 0:
                mat_90par[t_count,:] = par90sum/npix         
                mat_10par[t_count,:] = par10sum/npix      
                mat_per[t_count,:] = persum/npix  
                mat_npix[t_count] = npix
    #        print t_count      
            t_count = t_count + 1        
               
    ranges = np.linspace(3.8373,10011.6291,2623)
    
#    aac=[]
#    aacper=[]
#    aac1=[]
#    aac2=[]
#    aac3=[]
    new_res=space
    newbins=(np.shape(mat_90par)[1]-1)/new_res #23
    
    matPar90 = np.zeros(shape=[np.shape(mat_90par)[0],newbins])
    matPar10 = np.zeros(shape=[np.shape(mat_90par)[0],newbins])
    matPer = np.zeros(shape=[np.shape(mat_90par)[0],newbins])
#    matParc = np.zeros(shape=[np.shape(mat_90par)[0],newbins])
#    matPerc = np.zeros(shape=[np.shape(mat_90par)[0],newbins])
    
    for htime in range(0,np.shape(mat_90par)[0]):#np.linspace(1,24,24*2-1):
        
        import copy
        
        VPL90 = copy.copy((mat_90par)[htime,:])#[int(htime*(nt-1)/24),:])
        VPL10 = copy.copy((mat_10par)[htime,:])#[int(htime*(nt-1)/24),:])
        VPLper = copy.copy((mat_per)[htime,:])#[int(htime*(nt-1)/24),:])
        
        #VPL90=(VPL90-np.nanmean(VPL90[-150:]))
        #VPLper=(VPLper-np.nanmean(VPLper[-150:]))
            
        VPL90_2=np.zeros(shape=newbins)
        VPL10_2=np.zeros(shape=newbins)
        VPLper_2=np.zeros(shape=newbins)
        ranges2=np.zeros(shape=newbins)
        
        for i in range(newbins):
            ranges2[i] = np.nanmean(ranges[i*new_res:(i+1)*new_res])
            VPL90_2[i] = np.nanmean(VPL90[i*new_res:(i+1)*new_res])
            VPL10_2[i] = np.nanmean(VPL10[i*new_res:(i+1)*new_res])
            VPLper_2[i] = np.nanmean(VPLper[i*new_res:(i+1)*new_res])
            #if i < 18: print i,ranges2[i]
            
        P=copy.copy(VPL90_2)
        Pper=copy.copy(VPLper_2)
        r=copy.copy(ranges2)
        #pylab.plot(P)
        matPar90[htime,:]=P
        matPar10[htime,:]=copy.copy(VPL10_2)    
        matPer[htime,:]=Pper
            
    return[matPar90,matPar10,matPer, r]                

#mat_25022017 =  Lidar_space_time(date = "2017.02.25",space = 13, timee = 60)       
#mat_04102018 =  Lidar_space_time(date = "2018.10.04",space = 13, timee = 60)       
#mat_26022017 =  Lidar_space_time(date = "2017.02.26",space = 13, timee = 60)       
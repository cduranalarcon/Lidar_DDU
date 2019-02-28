def densplot(x,y,title="a)",bins = None, vmax = None, Range = None):
    import numpy as np
    import pylab
    
    def fmt(x, pos):
        a, b = '{:.1e}'.format(x).split('e')
        b = int(b)
        #return r'${} \times 10^{{{}}}$'.format(a, b)
        #print a == "0.0"
        print a,b
        if a != "0.0": 
            return r'$'+str(a)+'\xc2\xb7'.decode('utf8')+' 10^{{'+str(b)+'}}$'
        else:
            return r'$'+str(0)+'$' 

    h=np.histogram2d(x,y,bins=bins,range=Range)
    histo_temp=np.ma.masked_where(h[0] <= 0, h[0])
    extent = np.min(h[1]), np.max(h[1]), np.min(h[2]), np.max(h[2])

    histo_temp=100*histo_temp/(1.*np.nansum(histo_temp))

    if vmax==None: vmax=np.max(histo_temp)

    im=pylab.imshow(np.transpose(np.flip(((histo_temp)),1)),interpolation="nearest",
                    aspect='auto',extent=extent,vmin=0,vmax=vmax)
    
    #im=pylab.pcolor(np.linspace(0,2,bins[0]),np.linspace(0,2.9,bins[1]),
    #                np.transpose(histo_temp),vmin=0,vmax=vmax)
    
    if title != '': pylab.title(title)
    print extent
    return im

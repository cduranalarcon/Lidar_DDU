def fft_denoising(x, y, mu=1):
    import numpy as np
    import scipy.fftpack as fftp
    # get FFT
    myfft = fftp.rfft(y, np.size(x))
    
    #get filter
    t = np.linspace(-np.size(x)/2,np.size(x)/2-1,np.size(x))
    h = np.exp( -(t**2)/(2*mu**2));
    h = h/sum(h)
    
    factor = np.fft.fft(np.fft.fftshift(h)).real
    myfft = myfft*factor

    # make new series
    y2 = fftp.irfft(myfft)

    return [y2]
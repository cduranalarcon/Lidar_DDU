def running_mean(x, N):
    import numpy as np
    ini = (N-1)/2
    end = np.size(x)-(N-1)/2
    x2 = []
    for i in range(ini,end):
        x2.append(np.nanmean(x[i-(N-1)/2:i+(N-1)/2+1]))
    
    return np.array(x2)

def running_std(x, N):
    import numpy as np
    ini = (N-1)/2
    end = np.size(x)-(N-1)/2
    x2 = []
    for i in range(ini,end):
        x2.append(np.std(x[i-(N-1)/2:i+(N-1)/2+1]))
    
    return np.array(x2)
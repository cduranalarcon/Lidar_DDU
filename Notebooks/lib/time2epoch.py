def time2epoch(year, month,day,hour, minute = None):
    import numpy as np
    import time
    from calendar import timegm
    if np.size(hour) == 1:
        if minute == None:
            minute =int((hour - int(hour))*60)
            hour = int(hour)

        timestamp = str(year)+"-"+str(month).zfill(2)+"-"+str(day).zfill(2)+" "+str(hour).zfill(2)+":"+str(minute).zfill(2)+":00"

        utc_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        epoch_time = timegm(utc_time)
    else:
        epoch_time = []
        for h in hour:
            minute =int((h - int(h))*60)
            hour = int(h)

            timestamp = str(year)+"-"+str(month).zfill(2)+"-"+str(day).zfill(2)+" "+str(hour).zfill(2)+":"+str(minute).zfill(2)+":00"
            try:
                utc_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                epoch_time.append(timegm(utc_time))
            except:
                print 'Invalind date format : ' + timestamp
                    
    
    return np.array(epoch_time)
from datetime import datetime

now = datetime.now()
hour = now.hour
minute = now.minute
pm = False
if hour > 12:
    pm = True
    hour = hour - 12
    
hour = '{0:02d}'.format(hour)
minute = '{0:02d}'.format(minute)

ssd_h1 = hour[0]
ssd_h2 = hour[1]
ssd_m1 = minute[0]
ssd_m2 = minute[1]


def timeofday():
    if pm:
        return 'PM'
    else: return 'AM'
    
print(hour + ':' + minute + timeofday())
print('SSD 1: ' + ssd_h1)
print('SSD 2: ' + ssd_h2)
print('SSD 3: ' + ssd_m1)
print('SSD 4: ' + ssd_m2)



    

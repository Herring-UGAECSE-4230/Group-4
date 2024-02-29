from datetime import datetime

def getTime():
    global pm, ssd_h1
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    pm = False
    if hour > 12:
        pm = True
        hour = hour - 12
        
    hour = '{0:02d}'.format(hour)
    minute = '{0:02d}'.format(minute)

    ssd_h1 = int(hour[0])
    ssd_h2 = int(hour[1])
    ssd_m1 = int(minute[0])
    ssd_m2 = int(minute[1])
    return [ssd_h1, ssd_h2, ssd_m1, ssd_m2, pm]

curr = getTime()

def timeofday():
    global pm
    if pm:
        return 'PM'
    else: return 'AM'
    
print(('Current time is: {}{}:{}{}' + timeofday()).format(curr[0],curr[1],curr[2],curr[3]))



# while True:
#     getTime()
#     timeofday()
#     break
import time

# Define the start time
start_time = time.time()

# Set up a while loop
i = 0
while i < 1000000:
    i += 1
    # Measure the elapsed time
    elapsed_time = time.time() - start_time
    # Print the elapsed time within the loop
    print("Elapsed time:", elapsed_time, "seconds")

# Print the final elapsed time
print("Final elapsed time:", elapsed_time, "seconds")


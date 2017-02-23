import csv
from datetime import datetime, timedelta
import random
import sys

format = "%m/%d/%Y/%H:%M:%S"
d0 = datetime.strptime("01/01/1999/01:00:00", format)
num_datetimes = int(sys.argv[1])
out_file = sys.argv[2]

with open(out_file, 'w') as csvfile:
	datewriter = csv.writer(csvfile)
	datewriter.writerow([d0.strftime(format), 'A', 'B', 'message'])
	lastdate = d0
	for i in range(1, num_datetimes):
		delta = timedelta(	days = random.randint(0,6), 
									hours = random.randint(0,23),
									minutes = random.randint(0, 59), 
									seconds = random.randint(0, 59))
		lastdate = delta + lastdate 
		datewriter.writerow([lastdate.strftime(format), 'A', 'B', 'message'])

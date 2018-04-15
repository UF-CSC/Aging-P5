import sys,csv
import pandas as pd
import numpy as np

with open(sys.argv[1],'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        if row[3] == "0" or row[4] == "0": 
            print ", ".join(row)

#df = pd.read_csv(sys.argv[1])
#print df.loc[df['IS_CLOSED'] == 0]

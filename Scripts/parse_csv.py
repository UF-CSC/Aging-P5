import csv,sys,pickle

badList = []
with open(sys.argv[1],"r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[4] == "0" and row[-3] not in badList:
            badList.append(row[-3])
        if row[3] == "0" and row[-1] not in badList:
            badList.append(row[-1])
pickle.dump(badList,open(sys.argv[2],"w"))

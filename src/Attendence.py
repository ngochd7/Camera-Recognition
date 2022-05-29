import numpy as np 
from datetime import datetime

def markAttendance(name, isnew):
    with open('database/attendance.csv', 'r+', encoding='utf-8') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if isnew == True:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
        else:
            if name not in nameList:
                print("chwa co")
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
            
    f.close()
    return False

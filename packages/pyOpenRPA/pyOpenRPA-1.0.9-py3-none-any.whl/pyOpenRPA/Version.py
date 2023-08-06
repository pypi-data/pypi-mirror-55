import os
import re
#Just call Version.Get("..")
def Get(inFolderPath):
    lREPatternString="^v[0-9]*.[0-9]*.[0-9]*$"
    lResultList = [f for f in os.listdir(inFolderPath) if re.match(lREPatternString,f)]
    lResult=None
    if len(lResultList) == 0:
        lResult = None
    else:
        lResult = lResultList[0]
    return lResult
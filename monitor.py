import subprocess
import os
# from psutil import *
# import psutil
import getpass


currentUser = getpass.getuser()
print(currentUser)
currentDrive = os.environ['SYSTEMDRIVE']
print(currentDrive)

class process:

    def __init__(self, name, PID, path):
        self.name = name
        self.PID = PID
        self.path = path

    def getName(self):
        return self.name

    def getPID(self):
        return self.PID

    def getPath(self):
        return self.path
    def getValues(self):
        return [self.name, self.PID, self.path]


class process:

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getValues(self):
        return [self.name, self.path]


if __name__ == "__main__":
    cmd = 'WMIC PROCESS get Caption,Processid,ExecutablePath'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    commonDict = {}
    with open('commonProcesses.txt', 'r') as commonFile:
        for line in commonFile:
            line = line.split(',')
            commonDict[line[0]] = line[1]
    print(commonDict)

    processList = []
    f = open('processList.txt', 'a+')
    for line in proc.stdout:
        line = line.decode("utf-8")
        path = str()
        for start in range(0, len(line)):
            # if we have a start of a file path
            if line[start:start + 2] == 'C:':
                # windows maximum file path length is 260 TODO: account for //
                for end in range(0, 260):
                    if line[start + end: start + end + 4] == '.exe' or line[start + end: start + end + 4] == '.EXE':
                        path = line[start: start + end + 4]
                        break
        # TODO: get paths of services
        if path == '': continue
        words = line.split()
        newProcess = process(words[0], path)
        processList.append(newProcess)

    #snip off header
    processList = processList[1:]
    for item in processList:
        print(item.getValues())

# for service in psutil.win_service_iter():
#     sinfo = service.as_dict()
#     print("Name: {} Display name: {} Status: {} Type: {} Path: ".format(repr(sinfo["name"]), repr(sinfo["display_name"]), repr(sinfo["status"]), repr(sinfo["start_type"]), sinfo["binpath"]))
#     print(repr(sinfo["binpath"]))
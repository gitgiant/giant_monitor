#!/usr/bin/python
import subprocess
import os
import getpass
import ctypes

currentUser = getpass.getuser()
currentDrive = os.environ['SYSTEMDRIVE']

# Message Box
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


if __name__ == "__main__":
    cmd = 'WMIC PROCESS get Caption,Processid,ExecutablePath'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    defaultDict = {}
    # Load commonProcesses.txt into a dictionary
    with open('commonProcesses.txt', 'r') as commonFile:
        for line in commonFile:
            line = line.split(',')
            defaultDict[line[0]] = line[1]

    serviceList = []

    for line in proc.stdout:
        line = line.decode("utf-8")
        path = str()
        filename = str()
        # Read through a line and extract the filename and filepath, if there is no path then it is a service
        for start in range(0, len(line)):
            # skip the first line
            if "Caption" and "ExecutablePath" in line:
                continue
            # TODO: Extract filename with spaces
            # if we have a filename (ends with .exe)
            # if line[start:start+4] == '.exe':
            #     filename = line[0:start+4]
            #     print(filename)
            # if we have a start of a file path (starts with <currentDrive>:)
            if line[start:start + 2] == currentDrive:
                # windows maximum file path length is 260 TODO: account for //
                for end in range(0, 260):
                    if line[start + end: start + end + 4] == '.exe' or line[start + end: start + end + 4] == '.EXE':
                        path = line[start: start + end + 4]
                        break

        # TODO: get paths of services
        if path == '':
            words = line.split()
            serviceList.append(words)
            continue
        words = line.split()
        # check common paths for any replacements
        # If we have a common Process
        if words[0] in defaultDict:
            defaultPath = defaultDict[words[0]].rstrip('\n')
            if path != defaultPath:
                print("Replaced Running Process Detected!")
                print("File Name: " + words[0])
                print("File Path: " + path)
                print("Default Path: " + defaultPath)
                # Mbox returns 6 if user selects yes
                if (Mbox('Replaced Running Process Detected!', 'File Name: ' + words[0] + '\nFile Path: ' + path + '\nDefault Path: ' + defaultPath + '\nWould you like to upload this file to Virus Total?', 4)) == 6:
                    print("YES")
                else:
                    print("NO")

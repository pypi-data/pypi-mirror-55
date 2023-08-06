import subprocess

def ping(ipAddress, numberOfTimes=5):
    p = subprocess.Popen(["ping", "-c", str(numberOfTimes), ipAddress], stdout=subprocess.PIPE)
    out, err = p.communicate()
    print(out.decode('utf-8'))
    return out.decode('utf-8')

def findIP(verbose=True):
    p = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
    out, err = p.communicate()
    ipAddresses = out.decode('utf-8')
    linesplitIP = ipAddresses.split("\n")
    ipMap = [[], []]
    colonBool = False
    for val in linesplitIP:
        if ": flags" in val:
            ipMap[0].append(val.split(": flags")[0])
            colonBool = True
        elif colonBool:
            try:
                ipMap[1].append(val.split("inet ")[1].split(" netmask")[0])
                colonBool = False
            except IndexError:
                colonBool = False
                if verbose:
                    print("There was an issue finding an IP address for: ", ipMap[0][-1])
                    print("The ip information should be here: ", val)
                ipMap[1].append("N/A")

    currentAddresses = {}
    if len(ipMap[1]) == len(ipMap[0]):
        for i in range(len(ipMap[0])):
            currentAddresses[str(ipMap[0][i])] = str(ipMap[1][i]).strip()
    return currentAddresses

def ipChange(linkName, ipAddress, adminPassword):
    print("Changing IP Address for " + linkName + " to " + ipAddress)

    try:
        currentIP = findIP(False)[linkName]
        if currentIP == ipAddress:
            print("IP address is already set to the desired value!")
        else:
            for i in range(0, 3):
                p = subprocess.Popen("echo '" + adminPassword + "' | sudo -S ifconfig " + linkName + " " + ipAddress, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                currentIP = findIP(False)[linkName]
                if currentIP == ipAddress:
                    print("IP address set successfully!")
                    break
                else:
                    print("IP assignment failed! Current IP: " + currentIP)
    except KeyError:
        print("WARNING: The connection you're trying to change the IP Address for does not exist!!!")

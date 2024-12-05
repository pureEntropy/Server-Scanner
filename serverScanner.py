import json
import time
from mcstatus import JavaServer

def fullScan():
    jsonFile = open("out.json")
    data = json.loads(jsonFile.read())

    matchingFile = open('matchingServers.txt', 'w')
    outputFile = open('results.txt', 'w')
    idx = -1

    for obj in data:
        #print(obj['ip'])
        ip = obj['ip']
        #time.sleep(4)
        idx += 1

        try:
            server = JavaServer.lookup(ip)
            status = server.status()
        except IOError as e:
            print(f"{idx} | {ip} Error code: {e}")
            outputFile.write(f"{idx} | {ip} Error code: {e}")
            outputFile.write('\n')
            continue

        #if (status.version.name != 'Paper 1.19.2' or status.players.max != '50' or status.description != 'A Minecraft Server'):
        if (status.players.max != 50 or 'A Minecraft Server' not in status.description):
            print(f"{idx} | {ip}: did not match search.")
            outputFile.write(f"{idx} | {ip}: did not match search.")
            outputFile.write('\n')
            continue

        print(f"{idx} | ##### Matching Server IP: {ip} #####")
        matchingFile.write(f'IP: {ip}')
        matchingFile.write('\n')

    outputFile.close()
    matchingFile.close()
    jsonFile.close()


def singleScan(ip):
    try:
        server = JavaServer.lookup(ip)
        status = server.status()

        if (status.players.max != 50 or 'A Minecraft Server' not in status.description):
            print(f"{ip}: did not match search.")
            return
        
        print(f"""
Version: {status.version.name}
Protocol: {status.version.protocol}
Max Players: {status.players.max}
MOTD: {status.description}""")
    except IOError as e:
        print(f"{ip} | Error code: {e}")


def main():
    #fullScan()
    #singleScan(input('Server IP:'))
    #newProxy()
    massScan2()


def massScan2():
    rawScan = open("masscan_20221219.txt", "r")
    result = []
    for line in rawScan.readlines():
        if "65.109." in line:
            ip = line.split(' ')[3]
            print(f"##### {ip} #####")
            singleScan(ip)
            result.append(ip)

    print(result)


def newProxy():
    inputHostAddress = 68
    startingIP = inputHostAddress - 32
    endingIP = inputHostAddress + 32
    x = startingIP
    while(x <= endingIP):
        singleScan(f"65.109.{x}.176")
        x += 1
        


if __name__ == '__main__':
    main()
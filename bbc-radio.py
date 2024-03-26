#!/usr/bin/env python
import dotenv
import json
import random
import re
import requests
import subprocess
import sys

AUTH_ENV = 'auth.env'

# Currently, station discovery is not added, we are just getting the stream URL(s)

file = open('stations.json','r')
Content = json.load(file)
Stations = Content['stations']
file.close()
del file

callbacks       = Content['callback_url']
station_ids     = [s['id'] for s in Stations]
station_names   = [s["name"] for s in Stations]
names_lower     = [n.lower for n in Names]
Codes           = [s['code'] for s in Stations]
exportAll       = False
StreamAuth = dotenv.dotenv_values(AUTH_ENV)

def help():
    print(" = BBC Radio URI exporter =")
    print("  A tool to export BBC Radio streams")
    print("  You can get the new station ID from bbc.co.uk/sounds,")
    print("     you will see the ID at bbc.co.uk/sounds/play/live:<bbc_radio_station>")
    print("Usage: bbc-radio.py [-option] [fname]")
    print()
    print("Examples:")
    print(" bbc-radio.py -a # All national and regional stations")
    print(" bbc-radio.py -a -t N bbc_national.m3u # All national stations")
    print(" bbc-radio.py -a -b worst -t N bbc_mobile.m3u # smallest quality stream")
    print()
    print("  Note: When your GeoIP is outside the UK, you will get the non-UK streams.")
    print("     Sounds may or may not stop working outside the UK at some point.")
    print("     Account is currently not required outside the UK, or when not using the web/mobile app.")
    print("  -h --help               Show this help.")
    print("  -a --all                Export all stations of the specified types, to BBC-Radio.m3u")
    print("  -b --bitrate <bitrate>  Select bitrate: (best/worst/default) or (48..320) kbps; default=best")
    print("  -t --type    <type(s)>  Station type N)ational/R)egional/L)ocal (n/r/l); default=NR")
    print("     --reset-auth         Get new auth token.")
    exit()

def getStationId(a):
    a=a.strip()
    if a.isnumeric():
        return int(a)
    elif a in Codes:
        return Codes.index(ans)
    elif ans in Stations:
        return Stations.index(ans)
    elif ans.lower() in namesl:
        return Stations.index(namesl.index(ans.lower()))
    else:
        print(f"Couldn't find '{a}'.")
        return None

def saveNewJwtToken():
    station_id = random.choice(station_ids)
    content = requests.get("https://www.bbc.co.uk/sounds/play/live:{station_id}").text
    pattern = r'"liveStreamJwt": "([^"]*)"'
    match = re.search(pattern, content)
    if match:
        token = match.group(1)
        StreamAuth["jwt_auth"] = getJwtToken(station_ids[s])
        with open("auth.env","w") as file:
            file.write('\n'.join('='.join((i)) for i in StreamAuth.items()))
    else:
        print("Could not find jwt_token in script in HTML document")
        exit(1)
    


if not len(Names) == len(Stations) == len(Codes):
    print("Mismatching list lengths, Quitting...")

for i, arg in enumerate(sys.argv):
    if arg in {"-h", "-help", "--help"}:
        help()
        exit()
    elif arg in {"-a", "-all", "--all"}:
        exportAll = True
    elif arg in {"-b", "--bitrate", "-q", "--quality"}:
        Quality = sys.argv[i+1]
    elif arg in {"-t", "--type"}:
        _Types = sys.argv[i+1].lower()
    elif arg in {"-o", "--output"}:
        option = sys.argv[i+1]
        exportFileName = sys.stdout if option == "-" else option

TypeDict = {"n":"national","r":"regional","l":"local"}
RequestTypes = []
for t in TypeDict:
    if t in _Types:
        RequestTypes.append(TypeDict[t])
if not RequestTypes:
    RequestTypes = ["national","regional"]

if exportAll:
    exportFile = open("BBC-Radio.m3u","w")
    exportFile.write("#EXTM3U\n")

ans = ""
selected = []
i = 0
for station in stations:
    id = station["id"]
    name = station["name"]
    code = station["code"]
    type = station["type"]
    i += 1
    if exportAll:
        if type in RequestTypes:
            ans.append(code)
    else:
        print(f"[{i}] "+code.rjust(8) + ": '" + name + "' (" + station + ")")
        if i%15 == 0 and i != 0:
            if (input("More? (Y/n)").strip().lower()+" ")[0] in "naq":
                break

if exportAll:
    selected = [Stations.index(s) for s in Stations if s['type'] in RequestTypes]
elif exportChooser:
    print("Enter short code, or name, or index# (seperator: comma, and or space)")
    print("Enter 'done' when done")
    print("Enter 'd r1 r2 r3,r4' to delete")

    while ans != 'done': # select stations to export
        ans = input(': ').lower().strip().replace(' ',',')
        ans = ans.split(',')
        if ans[0] == "":
            continue
        if ans[0] == "done":
            break
        if ans[0] == 'd':
            for a in ans[1:]:
                id = getStationId(a)
                if id in selected:
                        selected.remove(id)
        if ans[0] in 'pd':
            print('\n'.join(f"{s}: {station_names[s]}" for s in selected))

        for a in ans:
            id = getStationId(a)
            for id in ids:
                if not id in selected:
                    selected.append(id)

hasError = False
for s in selected:
    request = requests.get(callbacks.format(station=station_ids[s],auth=StreamAuth["jwt_token"]))
    content = request.json()
    if content['result']:
        hasError = 'token'
        break
    elif request.ok:
        print(Names[s]+"(json):",)
    else:
        hasError = 'http'

if hasError:
    if hasError == 'token':
        print(f"Error occurred in API call: {content['result']}")
        if content['result'] == 'tokeninvalid':
            print("jwt_token token in invalid. Please check or reset it")
            print("Trying to get new jwt token")
            saveNewJwtToken()


input("Enter to exit...")

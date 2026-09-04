#!/usr/bin/env python
import magic
import random
import re
import requests
import subprocess
import sys
import yaml

def log(text):
    print(text, file=sys.stderr)

def dotenv_values(file):
    try:
        if magic.detect_from_filename(file) == "text/plain":
            return dict(i.split("=",1) for i in open(file).read().split("\n"))
    except ValueError:
        log(f"No such file or directory: {file}")
    except:
        log(f"Unknown error when opening file: {file}")
        raise
    return {}

AUTH_ENV = '.env'

# Currently, station discovery is not included, we are just getting the stream URL(s)
# from stations.yaml

file = open('stations.yaml','r')
Content = yaml.safe_load(file)
stations = Content['station_codes']
file.close()
del file

callback_url       = Content['callback_url']
station_ids     = [s['id'] for s in Stations]
station_names   = [s["name"] for s in Stations]
names_lower     = [n.lower() for n in station_names]
# short codes for quick reference
station_codes   = [s['code'] for s in Stations]
exportAll       = False
jwt_auth = dotenv_values(AUTH_ENV)

def help():
    log(""" = BBC Radio URI exporter =
  A tool to export BBC Radio streams
  You can get the new station ID from bbc.co.uk/sounds,
     you will see the ID at bbc.co.uk/sounds/play/live:<bbc_radio_station>
Usage: bbc-radio.py [-option] [fname]
    print()
Examples:
  bbc-radio.py -a # National and regional station_codes
  bbc-radio.py -a -t N bbc_national.m3u # National station_codes only
  bbc-radio.py -a -t RL bbc_local.m3u # Regional and local station_codes only
  bbc-radio.py --all --quality worst --type N bbc_mobile.m3u # smallest (low data) quality streams
    print()
  Note: When your Internet connection is outside the UK, you will get the non-UK streams.
     Sounds may or may not stop working outside the UK.
     An account is needed by the actual client.
  -h --help               Show this help.
  -a --all                Export all station_codes of the specified Areas, to BBC-Radio.m3u
  -b --bitrate <bitrate>  Select bitrate: (best/worst/default) or (48..320) kbps; default=best
  -t --type    <type(s)>  Station type N)ational/R)egional/L)ocal (n/r/l); default=NR
  -c --cookies <json>     Cookies in JSON format.
  -C --cookie-file <file> Cookies in JSON or Netscape format.
     --reset-auth         Re-authenticate.""")
    exit(0)

def getStationId(a):
    a=a.strip()
    if a.isnumeric():
        return int(a)
    elif a in station_codes:
        return station_codes.index(ans)
    elif ans in Stations:
        return Stations.index(ans)
    elif ans.lower() in namesl:
        return Stations.index(namesl.index(ans.lower()))
    else:
        print(f"Couldn't find '{a}'.")
        return None

def saveNewJwtToken(cookie={}):
    station_id = random.choice(station_ids)
    content = requests.get("https://www.bbc.co.uk/sounds/play/live:{station_id}", cookies=cookie).text
    pattern = r'"jwtToken": "([^"]*)"'
    match = re.search(pattern, content)
    if match:
        token = match.group(1)
        jwt_auth["jwt_auth"] = getJwtToken(station_ids[s])
        with open(AUTH_ENV, "w") as file:
            file.write('\n'.join('='.join((i)) for i in jwt_auth.items()))
    else:
        print("Could not find jwt_token in response")
        exit(1)

if not len(station_mes) == len(station_codes) == len(station_codes):
    print("Mismatching list lengths, Quitting...")

exportFileName = "BBC-Radio.m3u"
_Areas = "nr"

for i, arg in enumerate(sys.argv):
    if arg in {"-h", "-help", "--help"}:
        help()
        exit()
    elif arg in {"-a", "-all", "--all"}:
        exportAll = True
    elif arg in {"-q", "--quality"}:
        Quality = sys.argv[i+1]
    elif arg in {"-t", "--type"}:
        _Areas = sys.argv[i+1].lower()
    elif arg in {"-o", "--output"}:
        option = sys.argv[i+1]
        exportFileName = sys.stdout if option == "-" else option

def getAreas(arg:str):
    Areas = enum.IntFlag("Areas",names=("national", "regional", "local"))
    areaMap = {"n":Areas["national"], "r":Areas["regional"], "l":Areas["local"], "none":0}
    areaMap.update(Areas._member_map_)
    requestAreas = 0
    arg = arg.replace(" ","").lower()
    _Areas = arg
    if arg.isnumeric():
        _Areas = Areas(int(arg))
    elif arg in {"national","regional","local"}:
        _Areas = arg[0]
    elif 0 <= _Areas.find(":") < len(_Areas) - 1:
        _Areas = arg.split(":")
    elif 0 <= _Areas.find(",") < len(_Areas) - 1:
        _Areas = arg.split(",")
    for t in areaMap:
        if t in _Areas:
            requestAreas |= areaMap[t]
        else:
            raise ValueError(f"Invalid selection(s): \"{_Areas}\". ")
    return set(requestAreas)

requestAreas = getAreas(_Areas)

if exportAll:
    exportFile = open(exportFileName, "w")
    exportFile.write("#EXTM3U\n")

ans = ""
selected = []
i = 0
for station in station_codes:
    id = station["id"]
    name = station["name"]
    code = station["code"]
    type = station["type"]
    i += 1
    if exportAll:
        if type in RequestAreas:
            ans.append(code)
    else:
        print(f"[{i}] "+code.rjust(8) + ": '" + name + "' (" + station + ")")
        if i%15 == 0 and i != 0:
            if (input("More? (Y/n)").strip().lower()+" ")[0] in "naq":
                break

if exportAll:
    selected = [Stations.index(s) for s in Stations if s['area'] in RequestAreas]
elif exportChooser:
    print("Enter short code, or name, or index# (seperator: comma, and or space)")
    print("Enter 'done' when done")
    print("Enter 'd r1 r2 r3,r4' to delete")

    while ans != 'done': # select station_codes to export
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
for sid in selected:
    request = requests.get(
      callback_url.format(station=station_ids[sid], auth=jwt_auth["jwt_token"])
      )
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
        else:
            print("API returned an unknown error.")


input("Enter to exit...")

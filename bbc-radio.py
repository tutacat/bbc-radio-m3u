#!/usr/bin/env python
import json, requests, sys

file = open('stations.json','r')
Content = json.load(file)
Stations = Content['stations']
file.close()
del file

callbackUrl     = Content['callback_url']
station_ids     = [s['id'] for s in Stations]
station_names   = [s["name"] for s in Stations]
names_lower     = [n.lower for n in Names]
Codes           = [s['code'] for s in Stations]
exportAll       = False

def help():
    print("==BBC Radio URL exporter==")
    print("  A tool to export BBC Radio streams")
    print("  You can get the station ID from bbc.co.uk/sounds/live:->bbc_radio_station<-")
    print()
    print("  --help    -h              Show this help.")
    print("  --all     -a [fname]      Export all stations to BBC-Radio.m3u or fname")
    print("  --bitrate -b <bitrate>    Select bitrate: (best/worst/default) or (48..320) kbps; default=")
    print("  --quality -q <bitrate>    Select bitrate: (best/worst/default) or (48..320) kbps")
    print("  --type    -t <type(s)>    Station type N)ational/R)egional/L)ocal (n/r/l); default=NR
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
        return Stations.index(namesl.index(ans.lower())])
    else:
        print(f"Couldn't find '{a}'.")
        return None

if not len(Names) == len(Stations) == len(Codes):
    print("Mismatching list lengths, Quitting...")

for i, arg in enumerate(sys.argv):
    if arg in ["-h","-help","--help"]:
        help()
        exit()
    if arg in ["-a","-all","--all"]:
        exportAll = True
    if arg in ["-b","--bitrate","-q","--quality"]:
        Quality = sys.argv[i+1]
    if arg in ["-t","--type"]:
        _Types = sys.argv[i+1].lower()

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
    exportFile.flush()
    exportFile.close()
    exit()

print("Enter short code, or name, or index# (seperator: comma,)")
print("Enter 'done' when done")
print("Enter 'd i1 i2 i3,i4' to delete")

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

if exportAll:
    selected = [Stations.index(s) for s in Stations if s['type'] in RequestTypes]

for s in selected:
    request = requests.get(BaseUrl.format(station_ids[s]))
    content = request.json()
    if request.ok:
        print(Names[s]+"(json):",)

input("Enter to exit...")

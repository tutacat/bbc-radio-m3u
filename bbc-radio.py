#!/usr/bin/env python
import json, requests, sys

BaseUrl   =  "https://open.live.bbc.co.uk/mediaselector/6/select/version/2.0/mediaset/pc/vpid/{}/format/json/jsfunc/JS_callbacks0"
Stations  = ["bbc_radio_one","bbc_radio_one_dance","bbc_radio_one_relax","bbc_1xtra","bbc_radio_two","bbc_radio_three","bbc_radio_fourfm","bbc_radio_four_extra","bbc_radio_five_live","bbc_radio_five_live_sports_extra","bbc_6music","bbc_asian_network","bbc_world_service","bbc_radio_scotland_fm","bbc_radio_nan_gaidheal","bbc_radio_ulster","bbc_radio_foyle","bbc_radio_wales_fm","bbc_radio_cymru","bbc_radio_cymru_2","cbeebies_radio"]
Names     = ["Radio 1","Radio 1 Dance","Radio 1 relax","Radio 1Xtra","Radio 2","Radio 3","Radio 4","Radio 4 Extra","Radio 5 live","Radio 5 live sports extra","Radio 6 Music","Asian Network","World Service","Radio Scotland","Radio nan Gàidheal","Radio Ulster","Radio Foyle","Radio Wales","Radio Cymru","Radio Cymru 2","CBeebies Radio"]
namesl    = [n.lower for n in Names]
Codes     = ["1","1d","1r","1x","2","3","4","4x","5","5s","6","an","ws","scot","gaidheal","ulster","foyle","wales","cymru","cymru2","cbeebies"]
exportAll = False

def help():
    print("= BBC Radio URL exporter v0.1 =")
    print("  A tool to export BBC Radio streams")
    print("  You can get the station ID from bbc.co.uk/sounds/live:->bbc_radio_station<-")
    print()
    print("  --help    -h              Show this help.")
    print("  --all     -a              Export all stations to BBC-Radio.m3u")
    print("  --bitrate -b <bitrate>    Select bitrate: (best/worst/default) or (48..320) kbps")
    print("  --quality -q <bitrate>    Select bitrate: (best/worst/default) or (48..320) kbps")
    exit()

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

if exportAll:
    exportFile = open("BBC-Radio.m3u","w")
    exportFile.write("#EXTM3U\n")

i = 0
for code,name,station in zip(Codes,Names,Stations):
    i += 1
    if exportAll:
        StationUrl = json.loads(bytes(requests.get(BaseUrl.format(station)).content.replace(b"JS_callbacks0 ( ",b"").replace(b" );",b"")))["media"][-1]["connection"][-1]["href"]#.replace("https","http")
        print(f"{str(int(i/len(Codes)*100)).rjust(3)}% loading...",end="\r")
        #print(StationUrl)
        #exit()
        exportFile.write("#EXTINF:0,BBC - " + name + "\n" + StationUrl + "\n")
    else:
        print(code.rjust(8) + ": '" + name + "' (" + station + ")")
        if i%10 == 0 and i != 0:
            if (input("More? (Y/n)").strip().lower()+" ")[0] in "naq":
                break

if exportAll:
    exportFile.flush()
    exportFile.close()
    exit()
ans = ""
selected = []
while ans.strip()=="" or len(selected)==0: # select stations to export
    ans=input("Select a code or (station) (can be seperated by commas): ").lower()
    if ans.find(",")>-1:
        ans=ans.split(",")
    else:
        ans=[ans]
    for a in ans:
        a=a.strip()
        if a in Codes:
            selected += Stations[Codes.index(ans)]
        elif ans in Stations:
            selected += ans
        elif anslower() in namesl:
            selected += Stations[namesl.index(ans.lower())]
        else:
            print("Couldn't find '"+a+"'.")
if exportAll:
    selected = [i for i in range(len(Stations))]
for s in selected:
    request = requests.get(BaseUrl.format(Stations[s]))
    content = request.json()
    if request.ok:
        print(Names[s]+"(json):",)
input("Enter to exit...")

#!/usr/bin/env python3
import urllib.request
import json

if __name__ == "__main__":
    ld = {}
    td = {'EU':0,'US':0,'AU':0}
    for p in range(1,6):
        try:
            j = json.loads(urllib.request.urlopen('http://api.whelp.gg/corporation/98182803?page='+str(p)).read().decode())
        except urllib.error.HTTPError as err:
            if err.code == 404:
                break
            else:
                raise
        for i in j['kills']:
            ld.setdefault(i['system_name'],0)
            ld[i['system_name']] += 1
        for i in j['kills']:
            c = int(str(i['kill_time'])[11:13])
            if c >= 0 and c < 8:
                td['US']+=1
            elif c >= 8 and c < 16:
                td['AU']+=1
            elif c >= 16:
                td['EU']+=1
    sd = sorted(list(ld.items()), key=lambda p: -p[1])
    print("Kill System\n")
    print(str(sd)+"\n")
    st = sorted(list(td.items()), key=lambda p: -p[1])
    print("Kill TZ\n")
    print(st)

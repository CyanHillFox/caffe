import sys
import struct
#import device
import cxxfilt

print "Layer Name | Kernel Name/Layer Type | Start Time(ns) | End Time(ns) | Durations(ms) | GPU Occupancy | GPU IPC | GPU Util(%) | Mem OP(Level) | Temp(C) | Power(mW)"

met = open("mt/CUPTI_ACTIVITY_KIND_METRIC.csv").read().strip("index,_id_,id,value,correlationId,flags\n").split("0\n")[0:-1]

cormap = {}
for i in met:
    i = i.split(",")
    corid = i[-2]
    if corid not in cormap:
        cormap[corid] = []
    value = "".join(i[3:-2])
    if len(value) != 8:
        value = 0
    else:
        value = struct.unpack("d",value)[0]
    cormap[corid].append(value)

timetable = open("tl/CUPTI_ACTIVITY_KIND_CONCURRENT_KERNEL.csv").read().split("\n")[1:-1]
timetable_mt = open("mt/CUPTI_ACTIVITY_KIND_KERNEL.csv").read().split("\n")[1:-1]

nametable = open("tl/StringTable.csv").read().split("\n")[1:-1]
namep = {}
for i in nametable:
    ind = i.split(",")[0]
    nam = i.split(",")[-1]
    namep[ind] = nam

l = []
c = 0
for i in timetable:
    n = i.split(",")[-1]
    x = {} 
    x["start"]= int(i.split(",")[7])
    x["end"] = int(i.split(",")[8])
    x["name"] = cxxfilt.demangleb(namep[n])
    x["corid"] = timetable_mt[c].split(",")[-3]
    x["cordata"] = cormap[x["corid"]]
    l.append(x)
    c += 1

memtable = open("tl/CUPTI_ACTIVITY_KIND_MEMCPY.csv").read().split("\n")[1:-1]
for i in memtable:
    x = {}
    x["start"] = int(i.split(",")[7])
    x["end"] = int(i.split(",")[8])
    x["name"] = "cudaMemcpy"
    x["kind"] = int(i.split(",")[2])
    x["src"] = int(i.split(",")[3])
    x["dst"] = int(i.split(",")[4])
    x["size"] = int(i.split(",")[6])
    l.append(x)

memtable = open("tl/CUPTI_ACTIVITY_KIND_MEMSET.csv").read().split("\n")[1:-1]
for i in memtable:
    x = {}
    x["start"] = int(i.split(",")[4])
    x["end"] = int(i.split(",")[5])
    x["name"] = "cudaMemSet"
    x["size"] = int(i.split(",")[3])
    l.append(x)


layertable = open("tl/log").read().split("\n")[:-1]

sel = 0

starttime = 10000000000000000000
endtime =  -10000000000000000000
for i in layertable:
    try:
        i = i.split("]")[1]
        x = {}
        time = int(i.split(" ")[1])
        if time != sel:
            continue
        st = i.split(" ")[5]
        st = int(st.split(",")[0]) * 1000000000 + int(st.split(",")[1]) * 1000
        ed = i.split(" ")[7]
        ed = int(ed.split(",")[0]) * 1000000000 + int(ed.split(",")[1]) * 1000
        x["start"] = st
        if st < starttime:
            starttime = st
        x["end"] = ed
        if ed > endtime:
            endtime = ed
        x["name"] = "layer:" + i.split(" ")[2]
        x["type"] =  i.split(" ")[3]
        l.append(x)
    except:
        print(i)
        exit()

for x in l:
    x["du"] = (x["end"] - x["start"]) / 1000000.0

def cmp(a,b):
    if a["start"] > b["start"]:
        return 1
    elif a["start"] < b["start"]:
        return -1
    else:
        return 0

l.sort(cmp)
start = False
nowlayer = {}
oneshut = []
c = 0
ll = []
for i in l:
    if i["start"] >= starttime and i["end"] <= endtime:
        ll.append(i)
        if "type" in i:
            if nowlayer != {}:
                oneshut.append(nowlayer)
                nowlayer = {}
            nowlayer["name"] = i["name"]
            nowlayer["layer"] = i
            nowlayer["event"] = []
            continue
        nowlayer["event"].append(i)

oneshut.append(nowlayer)
       
#dev_inf = device.dev_info(starttime,endtime)

for i in oneshut:
    i["layer"]["start"] -= starttime
    i["layer"]["end"] -= starttime
    print i["layer"]["type"],"|",i["layer"]["name"],"|",i["layer"]["start"],"|",i["layer"]["end"],"|",i["layer"]["du"]
#    inlayer = [x for x in dev_inf if x["stamp"] >= i["layer"]["start"] and x["stamp"] <= i["layer"]["end"]]
#    gpu = [x["gpu"] for x in inlayer]
#    mem = [x["mem"] for x in inlayer]
#    tmp = [x["tmp"] for x in inlayer]
#    pow = [x["pow"] for x in inlayer]
#    if len(inlayer) == 0:
#        print ""
#    else:
#        print "||",
#        print "|",sum(gpu)/len(gpu), "|",sum(mem) / len(mem),"|", sum(tmp) / len(tmp),"|" ,sum(pow)/ len(pow)
    
    for j in i["event"]:
        j["start"] -= starttime
        j["end"] -= starttime
        print "|",j["name"],"|",j["start"],"|",j["end"],"|",j["du"],"|",
        if "cordata" in j and len(j["cordata"]) == 2:
            print j["cordata"][0], "|", j["cordata"][1]
        else:
            print ""
         
exit()
alllayer = {}
allkernel = {}
allmem = {}

for i in ll:
    if "type" in i:
        n = i["type"]
        if n not in alllayer:
            alllayer[n] = []
        alllayer[n].append(i["du"])
        continue
    if "size" in i:
        n = i["name"]
        if "kind" in i:
            n += str(i["kind"])
        if n not in allmem:
            allmem[n] = []
        allmem[n].append((i["size"],i["du"]))
        continue
    n = i["name"]
    if n not in allkernel:
        allkernel[n] = []
    allkernel[n].append(i["du"]) 


for i in alllayer:
    print i,"|",sum(alllayer[i]),"|",len(alllayer[i])
print ""
for i in allmem:
    print i,"|",reduce(lambda x,y: x + y[0],allmem[i], 0),"|",reduce(lambda x,y: x + y[1],allmem[i], 0),"|",len(allmem[i])
print ""
for i in allkernel:
    print i,"|",sum(allkernel[i]),"|",len(allkernel[i])


print ""

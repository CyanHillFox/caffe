import sys
loglist = open(sys.argv[1]).read().split("\n")[:-1]
al = {}
tp = {}
for logname in loglist:
    tp_map = {}
    log = open(logname).read().split("\n")
    for i in log:
        if "caffe.cpp:410" in i:
            x = i.split("type:")[1] 
            typ = x.split("forward:")[0].strip()
            tp[typ] = True
            tim = float(x.split("forward:")[1].split(" ")[1])
            if typ not in tp_map:
                tp_map[typ] = []
            tp_map[typ].append(tim)
    al[logname] = {}
    for i in tp_map:
        al[logname][i] = {"count":len(tp_map[i]), "sum": sum(tp_map[i])}

print ",",
for typ in tp:
    print typ,",,",
print ""

for logname in loglist:
    i = logname
    print i,",",
    for typ in tp:
        if typ not in al[i]:
            al[i][typ] = {}
            al[i][typ]["count"] = 0
            al[i][typ]["sum"] = 0.0
        print al[i][typ]["count"],",",al[i][typ]["sum"],",",
    print ""
    

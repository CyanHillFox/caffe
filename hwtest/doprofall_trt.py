import sys
import os
f = open(sys.argv[1]).read().split("\n")
gpu = "0"
if len(sys.argv) >2:
    gpu = sys.argv[2]
for i in f:
    n = i.split(" ")[0]
    out = i.split(" ")[1]
    cmd = "giexec --deploy=" + n + " --output=" + out + " --device=" + gpu + "  --batch=1 --iterations=1"
    l = os.popen(cmd).read().split("\n")
    for j in l:
        if "Average" in j:
            time = float(j.split(" ")[5])
            print n,time

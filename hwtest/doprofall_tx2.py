import sys
import os
f = open("proto.list").read().split("\n")[:-1]
for i in f:
    p = i.split(" ")[0]
    n = i.split(" ")[1]
    cmd = "./prof_tx.sh tx2 %s %s" %(p,n)
    print cmd
    os.system(cmd)

import sys
import os
f = open("proto.list").read().split("\n")[:-1]
for i in f:
    p = i.split(" ")[0]
    n = i.split(" ")[1]
    cmd = "./prof.sh ttxp %s %s" %(p,n)
    print cmd
    os.system(cmd)
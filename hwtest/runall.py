import sys
import os
net_list = open(sys.argv[1]).read().split("\n")[:-1]
for i in net_list:
    i = i.split(" ")[0]
    cmd = "caffe time -model %s -gpu 0 2> %s" % (i, "output/" + i.replace("/","_").split(".")[0] + ".log")
    print i
    os.system(cmd)
     

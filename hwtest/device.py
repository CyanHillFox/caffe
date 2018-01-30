import sys
def dev_info(start,end):
    f = open("device.log").read().split("\n")[:-1]
    l = []
    for i in f:
        x = {}
        gpu = int(i.split(" ")[0])  
        mem = int(i.split(" ")[1])
        tmp = int(i.split(" ")[2])
        pow = int(i.split(" ")[3])
        ts = int(i.split(" ")[4]) * 1000
        if ts >= start - 10000000 and ts <= end + 100000000:
            x["gpu"] = gpu
            x["mem"] = mem
            x["tmp"] = tmp
            x["pow"] = pow
            x["stamp"] = ts - start
#            print gpu,"|",mem,"|",tmp,"|",pow,"|" , ts - start    
            l.append(x)
    return l

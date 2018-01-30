import google.protobuf
import caffe
import sys
import caffe.proto.caffe_pb2 as caffe_pb2

proto = caffe_pb2.NetParameter()
net = caffe.Net(sys.argv[1],caffe.TEST)

google.protobuf.text_format.Merge(open(sys.argv[1]).read(), proto)

param = 0
cal = 0
n = 0

for i in proto.layer:
    name = i.name
    layer_blob = net.layer_dict[name].blobs
    top_blob = [net.blobs[j] for j in i.top]
    bottom_blob = [net.blobs[j] for j in i.bottom]
    typ = i.type
    layer_param = 0
    layer_cal = 0

    ic = ih = iw = 1
    oc = oh = ow = 1

    if len(bottom_blob) != 0:
        if len(bottom_blob[0].shape) > 0:
            n = bottom_blob[0].shape[0]
        if len(bottom_blob[0].shape) > 1:
            ic = bottom_blob[0].shape[1]
        if len(bottom_blob[0].shape) > 2:
            ih = bottom_blob[0].shape[2]
        if len(bottom_blob[0].shape) > 3:
            iw = bottom_blob[0].shape[3]
    if len(top_blob) != 0:
        if len(top_blob[0].shape) > 1:
            oc = top_blob[0].shape[1] 
        if len(top_blob[0].shape) > 2:
            oh = top_blob[0].shape[2] 
        if len(top_blob[0].shape) > 3:
            ow = top_blob[0].shape[3] 

    top_count =  oc * oh * ow

    if typ == "Convolution":
        k = i.convolution_param.kernel_size
        oc = i.convolution_param.num_output
        try:
            kw = k[0]
            kh = k[0]
        except:
            kw = i.convolution_param.kernel_w
            kh = i.convolution_param.kernel_h
        layer_cal = kw * kh * ic * top_count
        print "%s kernel: %d,%d,%d - (%d,%d,%d) -> %d,%d,%d, cal: %d" %(typ,ic,ih,iw,kh,kw,ic,oc,oh,ow, layer_cal),
    if typ == "Pooling":
        k = i.pooling_param.kernel_size
        kw = k
        kh = k
        layer_cal = kw * kh * ic * top_count
        print "%s kernel: %d,%d,%d - (%d,%d,%d) -> %d,%d,%d, cal: %d" %(typ,ic,ih,iw,kh,kw,ic,oc,oh,ow, layer_cal),
    if typ == "PReLU" or typ == "Eltwise" or typ == "TanH" or typ == "Scale" or typ == "BatchNorm" or typ == "ReLU" or typ == "Softmax" or typ == "Sigmoid" or typ == "LRN":
        layer_cal = top_count
        print "%s cal: %d" % (typ,layer_cal),
    if typ == "InnerProduct":
        layer_cal = ic * ih * iw * top_count
        print "%s cal: %d -> %d,%d" % (typ,ic * ih * iw, top_count, layer_cal),
    cal += layer_cal
         
        
    if len(layer_blob) != 0:
        for b in layer_blob:
            layer_param += b.count 
        param += layer_param
    print "layer name: %s, type: %s, param size: %d " % (name,typ,layer_param)

print "total param size : %d" % (param)
print "total cal : %d" % (cal)
   

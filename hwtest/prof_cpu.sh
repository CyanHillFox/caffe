export TABLE=table_$1
export NNAME=$3
mkdir ${TABLE}
mkdir ${TABLE}/${NNAME}
mkdir ${TABLE}/${NNAME}/tl
mkdir ${TABLE}/${NNAME}/mt
caffe time -model $2 -iterations 1 2>&1 | grep "caffe.cpp:400" > ${TABLE}/${NNAME}/tl/log
cd ${TABLE}/${NNAME}
python ../../timeline_cpu.py > ./result.csv

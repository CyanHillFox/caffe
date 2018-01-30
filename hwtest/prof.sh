export TABLE=table_$1
export NNAME=$3
mkdir ${TABLE}
mkdir ${TABLE}/${NNAME}
mkdir ${TABLE}/${NNAME}/tl
mkdir ${TABLE}/${NNAME}/mt
~/yufengwei/a.out > ${TABLE}/${NNAME}/device.log &
nvprof --unified-memory-profiling per-process-device -f -o ./${TABLE}/${NNAME}/tl/net.nvvp -- caffe time -model $2 -gpu 0 -iterations 1 2>&1 | grep "caffe.cpp:400" > ${TABLE}/${NNAME}/tl/log
killall a.out
python db.py ${TABLE}/${NNAME}/tl/net.nvvp ${TABLE}/${NNAME}/tl
nvprof -m ipc,achieved_occupancy -f -o ./${TABLE}/${NNAME}/mt/net.nvvp -- caffe time -model $2 -gpu 0 -iterations 1 2>&1 | grep "caffe.cpp:400" > ${TABLE}/${NNAME}/mt/log
python db.py ${TABLE}/${NNAME}/mt/net.nvvp ${TABLE}/${NNAME}/mt
cd ${TABLE}/${NNAME}
python ../../timeline.py > ./result.csv

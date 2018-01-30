nvprof --cpu-thread-tracing on  --system-profiling on -m achieved_occupancy,flop_sp_efficiency -f -o ~/model_test/reg/model/table_tx2/net.log -- caffe time -model $1 -gpu 0 -iterations 2 2>&1 | grep "caffe.cpp:400" > table_tx2/log
cd ~/model_test/reg/model/table_tx2
python db.py net.log
python timeline.py > $2.csv

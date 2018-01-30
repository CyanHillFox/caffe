nvprof --cpu-thread-tracing on  --system-profiling on -f -o ~/model_test/reg/model/table/net.log -- caffe time -model $1 -gpu 0 -iterations 2  2>&1 | grep "caffe.cpp:400" > table/log
cd ~/model_test/reg/model/table
python db.py net.log
python timeline.py > $2.csv

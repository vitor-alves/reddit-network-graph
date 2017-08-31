account=$1
password=$2
client_id=$3
secret=$4

# Search subreddits
#/usr/bin/python3 /home/hduser/redditMapReduce/searchReddit.py $account $password $client_id $secret

# Clean old stuff
/usr/local/hadoop/bin/hdfs dfs -rm -r /user/hduser/reddit-input /user/hduser/reddit-output
rm -r /home/hduser/redditMapReduce/redditEdges

# Copy search results from local to HDFS
/usr/local/hadoop/bin/hdfs dfs -mkdir /user/hduser/reddit-input
/usr/local/hadoop/bin/hdfs dfs -copyFromLocal /home/hduser/redditMapReduce/search_output.csv /user/hduser/reddit-input/search_output.csv

# Run Hadoop using streaming API
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.4.jar -D mapreduce.job.maps=16 -D mapreduce.job.reduces=16 \
-file /home/hduser/redditMapReduce/mapper.py    -mapper '/usr/bin/python3 /home/hduser/redditMapReduce/mapper.py' \
-file /home/hduser/redditMapReduce/reducer.py   -reducer '/usr/bin/python3 /home/hduser/redditMapReduce/reducer.py' \
-input /user/hduser/reddit-input/search_output.csv -output /user/hduser/reddit-output

# Copy result files from HDFS to local
mkdir /home/hduser/redditMapReduce/redditEdges
/usr/local/hadoop/bin/hdfs dfs -copyToLocal /user/hduser/reddit-output/* /home/hduser/redditMapReduce/redditEdges/
/usr/local/hadoop/bin/hdfs dfs -getmerge /user/hduser/reddit-output/ /home/hduser/redditMapReduce/redditEdges/edges.csv

# Add Source,Target to first line of edges.csv
sed  -i '1i Source,Target' /home/hduser/redditMapReduce/redditEdges/edges.csv

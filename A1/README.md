# MapReduce Instructions


### Requirements


This code is written in Python 3 and Hadoop 3.3. 
Please download the customer.csv and orders.csv.


### Run


Both MapReduce programms can be run either manually by piping the data through the scripts or with the Hadoop CLI.


**Manully with the scripts:**

<!-- #region -->
```bash 
cat {DataPath}/orders.csv {DataPath}/customers.csv | {TaskPath}mapper.py | {TaskPath}/reducer.py | sort > {TaskPath}/output.csv
```
<!-- #endregion -->

**With Hadoop CLI:**


1. Start signle node cluster.
2. Copy data from local path to HDFS storage:
    ```bash
    hadoop fs -copyFromLocal {DataPath} {HadoopDataPath}
    ```
3. Run hadoop streaming with `mapper.py` and `reducer.py`:

    ```bash
    hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar \
        -file {TaskPath}/mapper.py    -mapper {TaskPath}/mapper.py \
        -file {TaskPath}/reducer.py   -reducer {TaskPath}/reducer.py \
        -input {HadoopDataPath}/orders.csv {HadoopDataPath}/customer.csv -output /output/
    ```

4. Copy output to local path:
    ```bash
    hadoop fs -get /output/part-00000  {TaskPath}/output
    ```

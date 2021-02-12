package de.tuberlin.homework;

import org.apache.flink.api.common.functions.FlatJoinFunction;
import org.apache.flink.api.common.functions.JoinFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.operators.DeltaIteration;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.core.fs.FileSystem.WriteMode;
import org.apache.flink.util.Collector;

public class GraphShortestPath {
    public static final Integer FIRST_NODE = 17274;
    private static final String INPUT_FILE = "src/main/resources/ca-GrQc.txt";
    private static final String OUTPUT_FILE = "src/main/resources/output.csv";
    private static final String OUTPUT_SEPERATOR = " | ";
    
    public static void main(String[] args) throws Exception {
        // set up the execution environment
        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        // Use Dataset API to read tab seperated fiel:
        DataSet<Tuple2<Integer, Integer>> graphData = env.readCsvFile(INPUT_FILE).ignoreFirstLine().fieldDelimiter("\t")
                .types(Integer.class, Integer.class);

        
        // Calculate shortest paths with solution set: 17274, destination-node , path, cost
        DataSet<Tuple4<Integer, Integer, String, Integer>> solutionSet = graphData.map(new MapPaths()).distinct();  
        
        solutionSet.filter(path -> path.f3 == 1).print();


        int keyPosition = 1;
        DeltaIteration<Tuple4<Integer, Integer, String, Integer>, Tuple4<Integer, Integer, String, Integer>> iterator = solutionSet
                .iterateDelta(
                    solutionSet.filter(path -> path.f3 == 1), 20, keyPosition  // inital workset
                    );

        DataSet<Tuple4<Integer, Integer, String, Integer>> changes = iterator.getWorkset().join(graphData).where(1).equalTo(0).with(new JoinNextNode())
        .join(iterator.getSolutionSet()).where(1).equalTo(1).with(new Update());

        // Write output to file
        DataSet<Tuple4<Integer, Integer, String, Integer>> output = iterator.closeWith(changes, changes);

        output.filter(path -> path.f3 < Integer.MAX_VALUE).map(path -> path.f0 + OUTPUT_SEPERATOR + path.f1.toString()
                + OUTPUT_SEPERATOR + path.f2.toString() + OUTPUT_SEPERATOR + path.f3)
                .writeAsText(OUTPUT_FILE, WriteMode.OVERWRITE).setParallelism(1);

        // execute program
        env.execute("Calculate shortest path");
    }
}

final class MapPaths 
        implements MapFunction<Tuple2<Integer, Integer>, Tuple4<Integer, Integer, String, Integer>> {
    /**
     *
     */
    private static final long serialVersionUID = 1L;

    @Override
    public Tuple4<Integer, Integer, String, Integer> map(Tuple2<Integer, Integer> connection) throws Exception {
        // Check for starting node
        if (connection.f0 == 17274) {
            // path with cost 1
            return new Tuple4<>(GraphShortestPath.FIRST_NODE, connection.f1, String.valueOf(GraphShortestPath.FIRST_NODE) + ", " + connection.f1, 1);  
        };
        // Other nodes -> initial cost is max integer
        return new Tuple4<>(GraphShortestPath.FIRST_NODE, connection.f0, "", Integer.MAX_VALUE);
    }
}

final class JoinNextNode
        implements JoinFunction<Tuple4<Integer, Integer, String, Integer>, Tuple2<Integer, Integer>, Tuple4<Integer, Integer, String, Integer>> {
    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    @Override
    public Tuple4<Integer, Integer, String, Integer> join(Tuple4<Integer, Integer, String, Integer> vertex, Tuple2<Integer, Integer> edge) {
        //17274, destination-node , path, cost
        return new Tuple4<Integer, Integer, String, Integer>(vertex.f0, edge.f1, vertex.f2 + ", " + edge.f1, vertex.f3 + 1); 
    }
}

final class Update implements
        FlatJoinFunction<Tuple4<Integer, Integer, String, Integer>, Tuple4<Integer, Integer, String, Integer>, Tuple4<Integer, Integer, String, Integer>> {
    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    @Override
    public void join(Tuple4<Integer, Integer, String, Integer> current, Tuple4<Integer, Integer, String, Integer> old,
            Collector<Tuple4<Integer, Integer, String, Integer>> updated) {
        if (old != null && current.f3 < old.f3) { // Path to the node itself does not exist
            updated.collect(current); // Updates solution set if cost lower 
        }
    }

}

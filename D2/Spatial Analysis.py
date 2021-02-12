# # Spatial Data Analysis

# In this notebook:
# * Loading spatial data with geospark
# * Using JoinQuery without indexing
# * Trying different indexing methods

# ## Imports

import os

import folium
from time import time
import geopandas as gpd
import copy
from pyspark.sql import SparkSession
from geospark.core.SpatialRDD import PointRDD
from geospark.core.SpatialRDD import PolygonRDD
from pyspark import StorageLevel
from pyspark.sql import SQLContext
from geospark.register import GeoSparkRegistrator
from geospark.utils import GeoSparkKryoRegistrator, KryoSerializer
from geospark.register import upload_jars
from geospark.core.enums import FileDataSplitter
from geospark.core.spatialOperator import RangeQuery
from geospark.sql.types import GeometryType
from geospark.core.enums import IndexType
from geospark.core.spatialOperator import JoinQuery
from pyspark.sql.types import LongType
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from geospark.core.enums import GridType

# ## Environment

# %env SPARK_HOME /opt/conda/envs/geospark_demo/lib/python3.7/site-packages/pyspark
# %env ARROW_PRE_0_15_IPC_FORMAT 1
# %env JAVA_HOME /opt/conda/envs/geospark_demo

#Generate spark session
upload_jars()
spark = SparkSession.builder.\
        master("local[1]").\
        appName("TestApp").\
        config("spark.serializer", KryoSerializer.getName).\
        config("spark.kryo.registrator", GeoSparkKryoRegistrator.getName) .\
        getOrCreate()

GeoSparkRegistrator.registerAll(spark)

sc = spark.sparkContext
sqlContext = SQLContext(sc)

# ## Loading Data

data_path = "../../../data/HW2/nyc-data"
nyc_tweets_location = "file://" + os.path.abspath(data_path)+ "/nyc-tweets.txt"
nyc_neighborhoods_location = "file://" + os.path.abspath(data_path)+ "/nyc-neighborhoods.wkt"


# Loading point data set from twitter tweets 
def load_data():
    point_rdd = PointRDD(sc, nyc_tweets_location, 0, FileDataSplitter.CSV, False) #, 10, StorageLevel.MEMORY_ONLY, "epsg:4326", "epsg:4326")
    point_rdd.analyze()
    point_rdd.spatialPartitioning(GridType.KDBTREE)

    # Loading polygon dataset corresponding to the neighborhood regions in New York
    polygon_rdd = PolygonRDD(sc, nyc_neighborhoods_location, FileDataSplitter.WKT, False)
    polygon_rdd.spatialPartitioning(point_rdd.getPartitioner())
    return point_rdd, polygon_rdd


point_rdd, polygon_rdd = load_data()

# ## Without Index

# Finding the numbers of tweets that are contained within each one of the neighborhoord polygons without using spatial indexes.

start = time()
spatial_join_result_non_flat = JoinQuery.SpatialJoinQuery(point_rdd, polygon_rdd, False, False)
print(f"Finished after {time() - start} seconds")

start = time()
spatial_join_result_non_flat = JoinQuery.SpatialJoinQuery(point_rdd, polygon_rdd, False, False)
number_of_points = spatial_join_result_non_flat.map(lambda x: [x[0].geom, x[1].__len__()])
schema = StructType([
    StructField("neighborhood", GeometryType(), False),
    StructField("number_of_points", LongType(), False)
])
print(f"Finished after {time() - start} seconds")
df = spark.createDataFrame(number_of_points, schema, verifySchema=False)
df.show()

# Save
df.coalesce(1).toPandas().to_csv('output.csv',  index=False)

# ## With Indexing

# Finding the numbers of tweets that are contained within each one of the neighborhoord polygons using spatial indexes.

index_types = [IndexType.RTREE, False, IndexType.QUADTREE]

index_combinations = [
    (False, IndexType.RTREE),
    (False, IndexType.QUADTREE),
    (IndexType.RTREE, IndexType.RTREE),
    (IndexType.QUADTREE, IndexType.QUADTREE),
]
point_rdd, polygon_rdd = load_data()
for index in index_combinations:
    if index[0]:
        point_rdd.buildIndex(point_index, True)
    if index[1]:
        polygon_rdd.buildIndex(polygon_index, True)

    start = time()
    spatial_join_result_non_flat = JoinQuery.SpatialJoinQuery(
        point_rdd, polygon_rdd, True, False
    )
    print(f"\n Point index: {index[0]}, Polygon index: {index[1]}")
    print(f"Finished after {time() - start} seconds")

index_combinations = [(IndexType.RTREE, False), (IndexType.QUADTREE, False)]
point_rdd, polygon_rdd = load_data()
for index in index_combinations:
    if index[0]:
        point_rdd.buildIndex(point_index, True)
    if index[1]:
        polygon_rdd.buildIndex(polygon_index, True)

    start = time()
    spatial_join_result_non_flat = JoinQuery.SpatialJoinQuery(
        point_rdd, polygon_rdd, True, False
    )
    print(f"\n Point index: {point_index}, Polygon index: {polygon_index}")
    print(f"Finished after {time() - start} seconds")

srdd = polygon_rdd.setter

# +
# srdd.setter?
# -

from py4j.java_gateway import get_field

get_field(srdd.

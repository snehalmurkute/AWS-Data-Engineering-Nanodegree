import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node accelerometer_landing
accelerometer_landing_node1753142691219 = glueContext.create_dynamic_frame.from_catalog(database="stedi-human-balance", table_name="accelerometer_landing", transformation_ctx="accelerometer_landing_node1753142691219")

# Script generated for node customer_trusted
customer_trusted_node1754340742497 = glueContext.create_dynamic_frame.from_catalog(database="stedi-human-balance", table_name="customer_trusted", transformation_ctx="customer_trusted_node1754340742497")

# Script generated for node accelerometer_join_customer
SqlQuery0 = '''
select ds.user, ds.timestamp, ds.x, ds.y, ds.z from myDataSource ds
JOIN customer_trusted ct
ON ds.user = ct.email;
'''
accelerometer_join_customer_node1753142769927 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":accelerometer_landing_node1753142691219, "customer_trusted":customer_trusted_node1754340742497}, transformation_ctx = "accelerometer_join_customer_node1753142769927")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1753143081125 = glueContext.getSink(path="s3://datas3-fee5e117/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="accelerometer_trusted_node1753143081125")
accelerometer_trusted_node1753143081125.setCatalogInfo(catalogDatabase="stedi-human-balance",catalogTableName="accelerometer_trusted")
accelerometer_trusted_node1753143081125.setFormat("json")
accelerometer_trusted_node1753143081125.writeFrame(accelerometer_join_customer_node1753142769927)
job.commit()
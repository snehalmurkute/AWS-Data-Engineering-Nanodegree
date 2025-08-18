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

# Script generated for node step_trainer_landing
step_trainer_landing_node1753142691219 = glueContext.create_dynamic_frame.from_catalog(database="stedi-human-balance", table_name="step_trainer_landing", transformation_ctx="step_trainer_landing_node1753142691219")

# Script generated for node customer_curated
customer_curated_node1754340742497 = glueContext.create_dynamic_frame.from_catalog(database="stedi-human-balance", table_name="customer_curated", transformation_ctx="customer_curated_node1754340742497")

# Script generated for node step_trainer_join_customer_curated
SqlQuery0 = '''
select ds.serialNumber, ds.sensorReadingTime, 
ds.distanceFromObject from myDataSource ds
JOIN customer_curated cc
ON ds.serialnumber = cc.serialnumber;
'''
step_trainer_join_customer_curated_node1753142769927 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":step_trainer_landing_node1753142691219, "customer_curated":customer_curated_node1754340742497}, transformation_ctx = "step_trainer_join_customer_curated_node1753142769927")

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1753143081125 = glueContext.getSink(path="s3://datas3-fee5e117/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="step_trainer_trusted_node1753143081125")
step_trainer_trusted_node1753143081125.setCatalogInfo(catalogDatabase="stedi-human-balance",catalogTableName="step_trainer_trusted")
step_trainer_trusted_node1753143081125.setFormat("json")
step_trainer_trusted_node1753143081125.writeFrame(step_trainer_join_customer_curated_node1753142769927)
job.commit()
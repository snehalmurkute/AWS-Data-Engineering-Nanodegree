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

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1753160158747 = glueContext.create_dynamic_frame.from_catalog(database="stedi-human-balance", table_name="accelerometer_trusted", transformation_ctx="accelerometer_trusted_node1753160158747")

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1754345780902 = glueContext.create_dynamic_frame.from_catalog(database="stedi-human-balance", table_name="step_trainer_trusted", transformation_ctx="step_trainer_trusted_node1754345780902")

# Script generated for node machine_learning_curated
SqlQuery0 = '''
select * from step_trainer_trusted st
JOIN accelerometer_trusted at
ON at.timestamp = st.sensorReadingTime
'''
machine_learning_curated_node1753160118211 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"accelerometer_trusted":accelerometer_trusted_node1753160158747, "step_trainer_trusted":step_trainer_trusted_node1754345780902}, transformation_ctx = "machine_learning_curated_node1753160118211")

# Script generated for node machine_learning_curated
machine_learning_curated_node1753159996060 = glueContext.getSink(path="s3://datas3-fee5e117/step_trainer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="machine_learning_curated_node1753159996060")
machine_learning_curated_node1753159996060.setCatalogInfo(catalogDatabase="stedi-human-balance",catalogTableName="machine_learning_curated")
machine_learning_curated_node1753159996060.setFormat("json")
machine_learning_curated_node1753159996060.writeFrame(machine_learning_curated_node1753160118211)
job.commit()
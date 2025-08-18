import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
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

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node customer_landing
customer_landing_node1753142691219 = glueContext.create_dynamic_frame.from_catalog(database="stedi-human-balance", table_name="customer_landing", transformation_ctx="customer_landing_node1753142691219")

# Script generated for node Privacy Filter
SqlQuery706 = '''
select * from myDataSource
where shareWithResearchAsOfDate is not null;
'''
PrivacyFilter_node1753142769927 = sparkSqlQuery(glueContext, query = SqlQuery706, mapping = {"myDataSource":customer_landing_node1753142691219}, transformation_ctx = "PrivacyFilter_node1753142769927")

# Script generated for node customer_trusted
EvaluateDataQuality().process_rows(frame=PrivacyFilter_node1753142769927, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1753139724010", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
customer_trusted_node1753143081125 = glueContext.getSink(path="s3://datas3-fee5e117/customer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="customer_trusted_node1753143081125")
customer_trusted_node1753143081125.setCatalogInfo(catalogDatabase="stedi-human-balance",catalogTableName="customer_trusted")
customer_trusted_node1753143081125.setFormat("json")
customer_trusted_node1753143081125.writeFrame(PrivacyFilter_node1753142769927)
job.commit()
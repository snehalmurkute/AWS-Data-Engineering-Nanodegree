from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.secrets.metastore import MetastoreBackend
from airflow.utils.decorators import apply_defaults

BASE_COPY_COMMAND = """
        copy {} 
        from '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS JSON '{}'
        region 'us-west-2'
        TRUNCATECOLUMNS"""


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id: str,
                 aws_credentials_id: str,
                 table: str,
                 s3_url: str,
                 json_option: str = 'auto',
                 *args, **kwargs):
        """

        :param redshift_conn_id:
        :param aws_credentials_id:
        :param table:
        :param s3_url:
        :param json_option: auto(default) or jsonfilepath
        """
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_url = s3_url
        self.json_option = json_option

    def execute(self, context):
        self.log.info("Starting Data copy from {}".format(self.s3_url))
        aws_connection = MetastoreBackend().get_connection(self.aws_credentials_id)
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        redshift_hook.run(
            BASE_COPY_COMMAND.format(self.table, self.s3_url, aws_connection.login, aws_connection.password,
                                     self.json_option))
        self.log.info("Data copy finished")

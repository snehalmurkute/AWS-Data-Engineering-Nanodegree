from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

BASE_INSERT_SQL = """INSERT INTO {} {}"""


class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id: str,
                 table: str,
                 source_query: str,
                 *args, **kwargs):
        """

        :param redshift_conn_id:
        :param table:
        :param source_query:
        """
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.source_query = source_query

    def execute(self, context):
        self.log.info("Loading fact table {}".format(self.table))
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        redshift_hook.run(BASE_INSERT_SQL.format(self.table, self.source_query))

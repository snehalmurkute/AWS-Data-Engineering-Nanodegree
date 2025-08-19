from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

BASE_INSERT_SQL = """INSERT INTO {} {}"""


class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id: str,
                 table: str,
                 source_query: str,
                 insert_mode: str = "delete-load",
                 *args, **kwargs):
        """

        :param redshift_conn_id:
        :param table:
        :param source_query:
        :param insert_mode: options, insert or overwrite(default)
        """
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.source_query = source_query
        self.insert_mode = insert_mode

    def execute(self, context):
        self.log.info('Building dim table {}'.format(self.table))
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.insert_mode == "delete-load ":
            redshift_hook.run("TRUNCATE TABLE {}".format(self.table))

        redshift_hook.run(BASE_INSERT_SQL.format(self.table, self.source_query))

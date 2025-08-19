from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_conn_id, tests_and_expectations: dict, *args, **kwargs):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_hook = PostgresHook(postgres_conn_id=redshift_conn_id)
        self.tests_and_expectations = tests_and_expectations

    def execute(self, context):
        for the_test_and_expectation in self.tests_and_expectations:
            test = the_test_and_expectation['test']
            expected = the_test_and_expectation['expected']
            result = self.redshift_hook.get_first(test)
            if result and result[0] != expected:
                raise ValueError("The test {test} failed; expected: {expected}, actual: {result}".format(test=test, expected=expected, result=result[0]))

        self.log.info("All Data Quality Checks Passed Successfully!")

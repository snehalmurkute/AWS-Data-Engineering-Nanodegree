import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
        Loads raw data from S3 into staging tables in Redshift.

        This function runs a list of COPY commands to move data from
        S3 into temporary (staging) tables. These tables hold raw data
        before it's transformed and loaded into final tables.

        Parameters:
        cur : cursor
            Used to run SQL commands on the Redshift database.

        conn : connection
            Used to connect to the database and save the changes.

        Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        print(query)
        conn.commit()


def insert_tables(cur, conn):
    """
       Inserts data from staging tables into the final analytics tables.

       This function runs a list of SQL INSERT statements to move cleaned
       and transformed data from staging tables into the fact and
       dimension tables used for analysis.

       Parameters:
       cur : cursor
           Used to run SQL commands on the Redshift database.

       conn : connection
           Used to connect to the database and save the changes.

       Returns:
       None
    """
    for query in insert_table_queries:
        cur.execute(query)
        print(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
   # load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
        Drops all tables in the Redshift database.

        This function iterates over a list of SQL DROP TABLE statements and executes
        each one using the provided cursor. It commits each change to the Redshift
        database after execution.

        Parameters:
        cur : cursor
            Used to run SQL commands on the Redshift database.

        conn : connection
            Used to connect to the database and save the changes.

        Returns:
        None
    """
    for query in drop_table_queries:
        cur.execute(query)
        print(query)
        conn.commit()


def create_tables(cur, conn):
    """
        Creates all the tables in the Redshift database.

        This function runs a list of SQL queries to create the necessary tables.
        It uses the given database cursor to run each query and saves the changes
        after each one.

        Parameters:
        cur : cursor
            Used to run SQL commands on the Redshift database.

        conn : connection
            Used to connect to the database and save the changes.

        Returns:
        None
    """
    for query in create_table_queries:
        cur.execute(query)
        print(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
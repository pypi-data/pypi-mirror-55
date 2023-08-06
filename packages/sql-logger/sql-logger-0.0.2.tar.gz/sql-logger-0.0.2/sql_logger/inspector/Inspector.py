import yaml
import mysql
from sql_logger.inspector.Query import Query
from sql_logger.utils import connector


class Inspector:

    def __init__(self, filename):

        self._logging_information = self._read_config_file(filename)
        self._database_name = self._logging_information["log_info"]["database_name"]
        self._id = self._logging_information["log_info"]["id"]
        self._db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="pool",
            pool_size=5,
            **self._logging_information["sql_database"]
        )

    def get_query(self, table_name, condition=None):

        if condition is None or condition.lower() == 'all':
            condition = '1=1'  # In SQL, this means get all entries

        statement = "SELECT * FROM " + table_name + " WHERE " + condition

        try:
            list_of_matches = self._execute_query(statement)
        except mysql.connector.errors.ProgrammingError as e:
            raise ValueError("Cannot get query") from e
        else:
            header = self._execute_query("SHOW COLUMNS FROM "+table_name)
            query_ = Query(list_of_matches, [item[0] for item in header])
            return query_

    @staticmethod
    def _read_config_file(filename):

        with open(filename, 'r') as f:
            db1 = yaml.safe_load(f)

        return db1

    def _execute_query(self, statement):

        connection = connector.get_connection(self._db_pool)
        cursor = connection.cursor()

        try:
            cursor.execute("USE " + self._database_name)
        except mysql.connector.errors.ProgrammingError as e:
            raise e

        cursor.execute(statement)
        return_set = cursor.fetchall()
        connection.commit()
        connection.close()

        return return_set

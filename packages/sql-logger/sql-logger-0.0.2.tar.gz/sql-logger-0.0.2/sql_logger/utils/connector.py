import mysql


def get_connection(pool):
    while True:
        try:
            connection = pool.get_connection()
        except mysql.connector.errors.PoolError:
            continue
        else:
            break

    return connection

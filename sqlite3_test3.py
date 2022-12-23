import sqlite3
from sqlite3 import Error
from types import SimpleNamespace

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def set_Globals():
    Gloval = SimpleNamespace()
    Gloval.db_name = r"faceencodings.db"
    return Gloval

def main():
    Gloval = set_Globals()

    # create a database connection
    conn = create_connection(Gloval.db_name)

    with conn:
        update_task(conn, (2, '2015-01-04', '2015-01-06', 2))


if __name__ == '__main__':
    main()
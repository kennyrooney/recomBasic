import sqlite3
from utils import get_hashed_password


sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    email text PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL


                                ); """
jokes_string = ','.join(['joke{} integer DEFAULT 0'.format(x) for x in range(100)])
sql_create_joke_rating_table = """ CREATE TABLE IF NOT EXISTS joke_ratings (
                                    user_id text PRIMARY KEY,
                                    {},

                                    FOREIGN KEY (user_id) REFERENCES users (email)
                                ); """.format(jokes_string)

sql_create_pass_table = """CREATE TABLE IF NOT EXISTS passwords (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                password BLOB NOT NULL,
                                user_id text NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users (email)
                            );"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except conn.Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except conn.Error as e:
        print(e)


#database = "C:\\Users\scott\db\login.db"
#conn = create_connection(database)

#create_table(conn, sql_create_users_table)
#create_table(conn, sql_create_pass_table)


def create_user(conn, user):
    """
    Create a new user into the users table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO users(email,first_name,last_name)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def create_password(conn, password):
    """
    Create a new password into the password table
    :param conn:
    :param password:
    :return: project id
    """
    sql = ''' INSERT INTO passwords(password,user_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, password)
    return cur.lastrowid

#
# user = ('slmatton@comcast.net', 'Scott', 'Matton')
#
# pw = '12345'
#
# pass_data = (get_hashed_password(pw.encode()), 'slmatton@comcast.net')
# create_user(conn, user)
# create_password(conn, pass_data)
# conn.commit()
# conn.close()
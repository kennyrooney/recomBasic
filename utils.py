import dash_html_components as html
import os
import bcrypt
import sqlite3
import random
import json
from appConfig import jokes_folder, sqlite3_db


def makeIframe(file_name, no_frame=False):
    if no_frame:
        f = os.path.join(jokes_folder, file_name)
        _, extension = os.path.splitext(f)

        msg = open(f).read()
        return html.Iframe(sandbox='', srcDoc=msg, style={'width': "80%", 'height': 400})

    else:
        if file_name is not None:
            f = os.path.join(jokes_folder, file_name)
            _, extension = os.path.splitext(f)
            message1 = ''
            with open(f) as file1:
                for line in file1:
                    if extension.lower() == '.xml':
                        line = line.replace("<", "&lt").replace(">", "&gt")
                    message1 = message1 + line + '<BR>'

            return html.Iframe(sandbox='', srcDoc=message1, style={'width': "50%", "height": 400})
        else:

            return None


def getFiles():
    files = os.listdir(jokes_folder)
    file_options = [{'label': x, 'value': x} for x in files]
    return file_options


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


def query_password(user):
    """
    Query database for user password
    :param user:
    :return:
    """
    conn = create_connection(sqlite3_db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    t = ("{}".format(user),)
    c.execute("select password from passwords where user_id =?", t)
    r = c.fetchone()
    if r is None:
        password = None
    else:
        password = tuple(r)[0]
    conn.close()

    return password


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


def makeJokeOrder(jokes_path):
    '''
    Jokes file names look like init84.html
    :return:
        list of joke paths
    '''
    jokes_files = os.listdir(jokes_path)
    random.shuffle(jokes_files)

    jokes_paths = [os.path.join(jokes_path, x) for x in jokes_files]

    return json.dumps([jokes_paths, 0, 0, 0])


def update_rating(conn, update_dict):
    """
    update jokeN for user_id
    :param conn:
    :param update_dict:
    :return: project id
    """
    jokeid, jokerating = update_dict['joke']
    user = update_dict['user']
    sql = ''' UPDATE joke_ratings
              SET {} = ? 
              WHERE user_id = ?; 
              '''.format(jokeid, jokeid)
    sql2 = '''INSERT or IGNORE INTO  joke_ratings({},user_id) VALUES(?,?); '''.format(jokeid, jokeid)

    cur = conn.cursor()
    cur.execute(sql, (jokerating, user))
    cur.execute(sql2, (jokerating, user))


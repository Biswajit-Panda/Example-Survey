from os import name
from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime
import pandas as pd
from sqlite3 import Error


# Create the Flask app
app = Flask(__name__)


DATABASE_USER = "databasesqlite.db"
DATABASE_QUESTION = "questionsqlite.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_database():

    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        email text NOT NULL UNIQUE,
                                        name text NOT NULL
                                    ); """

    sql_create_question_table = """ CREATE TABLE IF NOT EXISTS question (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        qid integer NOT NULL,
                                        uid integer NOT NULL,
                                        time text NOT NULL,
                                        rating text NULL,
                                        desc text NULL,
                                        FOREIGN KEY (uid) REFERENCES user (id)
                                    ); """

    # create a user database connection
    conn = create_connection(DATABASE_USER)

    # create tables
    if conn is not None:
        # create survey table
        create_table(conn, sql_create_user_table)
        # close database connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

    # close database connection
    conn.close()
    # create a question database connection
    conn = create_connection(DATABASE_QUESTION)

    # create tables
    if conn is not None:
        # create survey table
        create_table(conn, sql_create_question_table)
        # close database connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

    # close database connection
    conn.close()


def insert_data(conn, dname, data):
    """
    Create a new row into the survey table
    :param conn:
    :param data:
    """
    if dname == 'user':
        sql = ''' INSERT INTO user(email, name) VALUES(?,?) '''
    elif dname == 'question':
        sql = ''' INSERT INTO question(qid, uid, time, rating, desc) VALUES(?,?,?,?,?) '''
    else:
        print('table not found')
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

# Home Page


@app.route('/')
def home():
    create_database()
    return render_template('index.html')

# Prediction Function


@app.route('/submission', methods=['POST'])
def submission():
    '''
    For rendering results on HTML GUI
    '''
    # all_data = tuple([x for x in request.form.values()])
    if request.method == "POST":
        # all_data = tuple([x for x in request.form.values()])
        u_naem = request.form['u_name']
        email = request.form['email']
        q01_01 = request.form['q01_01']
        rating_01_01 = request.form['rating_01_01']
        q01_02 = request.form['q01_02']
        rating_01_02 = request.form['rating_01_02']
        q02_01 = request.form['q02_01']
        rating_02_01 = request.form['rating_02_01']
        q02_02 = request.form['q02_02']
        rating_02_02 = request.form['rating_02_02']
        qstns = [("q01_01", q01_01, rating_01_01), ("q01_02", q01_02, rating_01_02),
                 ("q02_01", q02_01, rating_02_01), ("q02_02", q02_02, rating_02_02)]

        # all_data = (rating, q1, q2, q3, q4, q5, comment)
    # create a database connection
    conn_user = create_connection(DATABASE_USER)
    conn_qstn = create_connection(DATABASE_QUESTION)
    cur = conn_user.cursor()
    cur.execute("SELECT id FROM user WHERE email = ?", (email,))
    data = cur.fetchall()
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if len(data) == 0:
        insert_data(conn_user, 'user', (email, u_naem))
        curser = conn_user.cursor()
        curser.execute("SELECT id FROM user WHERE email = ?", (email,))
        uid = curser.fetchall()
        for item in qstns:
            insert_data(conn_qstn, 'question',
                        (item[0], uid[0][0], time, item[2], item[1]))
    else:
        for item in qstns:
            insert_data(conn_qstn, 'question',
                        (item[0], data[0][0], time, item[2], item[1]))

    return render_template('success.html', data=data)


@app.route('/view_database')
def view_database():
    conn = create_connection(DATABASE_QUESTION)
    cur = conn.cursor()
    cur.execute("SELECT * FROM question")
    rows_qstn = cur.fetchall()
    conn.close()
    conn = create_connection(DATABASE_USER)
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows_user = cur.fetchall()
    conn.close()
    conn = sqlite3.connect(DATABASE_QUESTION, isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM question", conn)
    db_df.to_csv('static/assets/survey_desc.csv', index=False)
    conn.close()
    conn = sqlite3.connect(DATABASE_USER, isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM user", conn)
    db_df.to_csv('static/assets/user_details.csv', index=False)
    conn.close()
    return render_template('showdata.html', data_user=rows_user, data_qstn=rows_qstn)


if __name__ == "__main__":
    app.run(debug=True)

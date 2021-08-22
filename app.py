from flask import Flask, request, jsonify, render_template
import sqlite3
from sqlite3 import Error


# Create the Flask app
app = Flask(__name__)


DATABASE = "surveysqlite.db"


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

    sql_create_survey_table = """ CREATE TABLE IF NOT EXISTS survey (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        rating integer NOT NULL,
                                        qstn1 text NOT NULL,
                                        qstn2 text NOT NULL,
                                        qstn3 text NOT NULL,
                                        qstn4 text NOT NULL,
                                        qstn5 text NOT NULL,
                                        comment text
                                    ); """

    # create a database connection
    conn = create_connection(DATABASE)

    # create tables
    if conn is not None:
        # create survey table
        create_table(conn, sql_create_survey_table)
        # close database connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

    # close database connection
    conn.close()


def insert_data(conn, data):
    """
    Create a new row into the survey table
    :param conn:
    :param data:
    """
    sql = ''' INSERT INTO survey(rating,qstn1,qstn2,qstn3,qstn4,qstn5,comment) VALUES(?,?,?,?,?,?,?) '''
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
    all_data = tuple([x for x in request.form.values()])
    # all_data = (2 , 'abc', 'bcs', 'wer', 'rew', 'gdw', 'awx')
    # create a database connection
    conn = create_connection(DATABASE)
    # insert data into database
    insert_data(conn, all_data)
    # close database connection
    conn.close()

    return render_template('success.html', data=all_data)


@app.route('/view_database')
def view_database():
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM survey LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    return render_template('showdata.html', data=rows)


if __name__ == "__main__":
    app.run(debug=True)

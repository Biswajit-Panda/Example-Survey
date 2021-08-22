from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


# Create the Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://szncamievaihiu:52518d2fe20fceb36e2c882a90ec4189081f3afd16faee96fa40acea11b9dc3d@ec2-18-214-238-28.compute-1.amazonaws.com:5432/d7gprejmg7guvd'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# database skeliton


# class UserDetails(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50), unique=True)
#     name = db.Column(db.String(50))

#     def __init__(self, email, name):
#         self.email = email
#         self.name = name


# class Questions(db.Model):
#     __tablename__ = 'question'
#     id = db.Column(db.Integer, primary_key=True)
#     qstn_id = db.Column(db.Integer)
#     qstn_desc = db.Column(db.String(200))
#     user_id = db.Column(db.Integer)
#     time = db.Column(db.String(30))
#     rating = db.Column(db.Integer)
#     desc = db.Column(db.String(200))

#     def __init__(self, qstn_id, qstn_desc, user_id, time, rating, desc):
#         self.qstn_id = qstn_id
#         self.qstn_desc = qstn_desc
#         self.user_id = user_id
#         self.time = time
#         self.rating = rating
#         self.desc = desc


class Temp(db.Model):
    __tablename__ = 'survey'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(200))
    q1 = db.Column(db.String(200))
    q2 = db.Column(db.String(200))
    q3 = db.Column(db.String(200))
    q4 = db.Column(db.String(200))
    q5 = db.Column(db.String(200))
    comment = db.Column(db.String(200))

    def __init__(self, rating, q1, q2, q3, q4, q5, comment):
        self.rating = rating
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.comment = comment


# db.create_all()

# Home Page


@app.route('/')
def home():
    return render_template('index.html')

# Prediction Function


@app.route('/submission', methods=['POST'])
def submission():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == "POST":
        # all_data = tuple([x for x in request.form.values()])
        rating = request.form['star']
        q1 = request.form['question_1']
        q2 = request.form['question_2']
        q3 = request.form['question_3']
        q4 = request.form['question_4']
        q5 = request.form['question_5']
        comment = request.form['comment']

        all_data = (rating, q1, q2, q3, q4, q5, comment)

        # if db.session.query(UserDetails).filter(UserDetails.email == email).count() == 0:
        #     u_data = UserDetails(email, name)
        #     db.session.add(u_data)
        #     db.session.commit()
        # else:
        #     pass
        t_data = Temp(rating, q1, q2, q3, q4, q5, comment)
        db.session.add(t_data)
        db.session.commit()

        return render_template('success.html', data=all_data)
    return render_template('success.html', data='Data not found')


@app.route('/view_database')
def view_database():
    return render_template('showdata.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import json 

config = {
  "apiKey": "AIzaSyA3YUcfrfUyGWoCRwgjIJmZmDQXOPcmOFU",
  "authDomain": "casestudy-14f76.firebaseapp.com",
  "projectId": "casestudy-14f76",
  "storageBucket": "casestudy-14f76.appspot.com",
  "messagingSenderId": "425743409507",
  "appId": "1:425743409507:web:975b709c91f3fd2ceeb356",
  "measurementId": "G-Z6948G4N3V",
  "databaseURL": "https://casestudy-14f76-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


def find_user_through_email(email):
    for user in db.Child('Users').get().val():
        user_dict = json.loads(json.dumps(db.child('Users').get().val()))

        if user_dict['email'] == email:
            second_user_localId = user
            second_user_name = user_dict['name']
            final_second_user_dict = user_dict
    return [second_user_localId, second_user_name, final_second_user_dict]


# def add(need):

    # roomsx = db.child("rooms").child(login_session['room']['localId']).get().val()  
    # if dict(roomsx)['needs'] == '' :
    #     needs = {'needs': [""]}
    #     roomsx = db.child("rooms").child(login_session['room']['localId']).get().val()
    #     print('bad')
    #     needs = {"needs": [need]}
    #     db.child("rooms").child(login_session['room']['localId']).update(needs)
    # else:
    #     roomsx = db.child("rooms").child(login_session['room']['localId']).get().val()
    #     needs = dict(roomsx)['needs']
    #     needs = needs.append(need)
    #     db.child("rooms").child(login_session['room']['localId']).set(needs)

@app.route ('/signin', methods = (['GET', 'POST']))
def signin():
    error = ""
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        state = request.form['job']
        user = user + '@gmail.com'
        # try:
        if state == 'nurse':
            login_session['nurse'] = auth.sign_in_with_email_and_password(user, password)
            return redirect(url_for('home'))
        if state == 'patient':
            login_session['room'] = auth.sign_in_with_email_and_password(user, password)
            return redirect(url_for('home'))
    # except:
        error = "smth went wrong"
        return error
    return render_template('signin.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == "POST":
        user = request.form['username']
        password = request.form['password']
        state = request.form['job']
        user = user + '@gmail.com'
        if state == 'patient':
            login_session['room'] = auth.create_user_with_email_and_password(user, password)
            room = {'room_num': user, 'password': password, 'needs': ""}
            db.child('rooms').child(login_session['room']['localId']).set(room)
        else:
            email = request.form['email']
            user = request.form['username']
            phone_number = request.form['phone_number']
            login_session['nurse'] = auth.create_user_with_email_and_password(email, password)
            nurse = {'nurse_name': user, 'password': password, 'email': email, 'phone_number': phone_number}
            db.child('nurses').child(login_session['nurse']['localId']).set(nurse)
        return redirect(url_for('home'))

    return render_template("signup.html")



@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/sos')
def sos():
    return render_template('sos.html') 

@app.route('/help')
def help():
    return render_template('general_help.html') 

@app.route('/medicine')
def medicine():
    return render_template('medicine.html')


@app.route('/nurse')
def nurse():
    # add('nurse')
    return render_template('nurse.html')

@app.route('/supplies')
def supplies():
    # add('supplies')
    return render_template('supplies.html')     

@app.route('/ye')
def ye():
    return render_template('test.html')

@app.route('/login')
def login():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug = True)
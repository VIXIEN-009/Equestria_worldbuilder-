from flask import Flask , render_template, request,flash, session, redirect
import sqlite3 

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route( '/' )
def index():
    return render_template('index.html')

@app.route( '/signup', methods=['GET', 'POST'])
def signup():
    print(request.form)
    if request.method == 'GET':
        return render_template('signup.html', passwords_dont_match=False)
    elif request.form['psw'] != request.form['psw-repeat']:
        return render_template('signup.html', passwords_dont_match=True)
    else:
        redirect('/')



@app.route( '/login' )
def login():
    return render_template('login.html')

@app.route( '/libary' )
def libary():
    return render_template('libary.html')


if __name__ == "__main__":
    app.run(debug=True)
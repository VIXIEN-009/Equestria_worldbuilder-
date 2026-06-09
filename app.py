from flask import Flask , render_template
import sqlite3 

app = Flask(__name__)

@app.route( '/' )
def index():
    return render_template('index.html')

@app.route( '/signup' )
def signup():
    return render_template('signup.html')

@app.route( '/login' )
def login():
    return render_template('login.html')

@app.route( '/libary' )
def libary():
    return render_template('libary.html')


if __name__ == "__main__":
    app.run(debug=True)
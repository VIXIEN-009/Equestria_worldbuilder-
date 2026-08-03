from flask import Flask , render_template, request,flash, session, redirect
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

DB = 'db.db'
app.config['SECRET_KEY'] = "SecretStarlightGlimmerKey"

def query_db(sql, args=(), one=False):
    """Connect to the db and run the provided query
    Returns a list of dicts, a single dict OR an error
    Will also execute INSERT, UPDATE and DELETE
    """

db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row
cursor = db.cursor()

@app.route( '/' )
def index():
    return render_template('index.html')

@app.route( '/signup', methods=['GET', 'POST'])
def signup():
    print(request.form)
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['psw']
        hashed_password = generate_password_hash(password)
        sql = "INSERT INTO user (email,username,psw) VALUES (?,?,?)"
        res = query_db(sql,(email,username,hashed_password))
        flash("Sign Up Successful")
        redirect('/')
    return render_template('signup.html')
    



@app.route( '/login', methods=["GET", "POST"] )
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['psw']
        sql = "SELECT * FROM user WHERE username = ?"
        user = query_db(sql=sql, args=(username,),one=True)
        if user:
            if check_password_hash(user['psw'] ,password):
                session['user'] = user
                flash("logged in sucessfully")
                redirect_location = request.args.get('redirect')

                if redirect_location:
                    return redirect("/" + redirect_location)
                else:
                    return redirect('/')
    
@app.route( '/libary' )
def libary():
    return render_template('libary.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
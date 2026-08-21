from flask import Flask , render_template, request,flash, session, redirect
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB = 'database.db'
app.config['SECRET_KEY'] = "SecretStarlightGlimmerKey"

def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results

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

        sql = "INSERT INTO user (username,password) VALUES (?,?)"
        query_db(sql,(email, username,hashed_password))
        flash("Sign Up Successful")
    return render_template('signup.html')




@app.route( '/login', methods=["GET", "POST"] )
def login():
    print(request.form)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE username = ?"
        user = query_db(sql=sql, args=(username,),one=True)
        if user:
            if check_password_hash(user['psw'] ,password):
                session['user'] = user
                flash("logged in sucessfully")
                redirect('/')
    return render_template('login.html')
    
@app.route( '/libary' )
def libary():
    return render_template('libary.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(debug=True)
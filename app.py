from flask import Flask , render_template, request, flash, session, redirect
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
from livereload import Server
from pathlib import Path 

app = Flask(__name__)

DB = 'database.db'
app.config['SECRET_KEY'] = "SecretStarlightGlimmerKey"

UPLOAD_here = Path('static/UPlOAD')

def query_db(sql,args=(),one=False):
    """Connect to the db and run the provided query
    Returns a list of dicts, a single dict OR an error
    Will also execute INSERT, UPDATE and DELETE
    """
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    try:
        cursor.execute(sql, args)
        results = [dict(row) for row in cursor.fetchall()]
        db.commit()

        if not results:
            return None
        if one:
            return results[0]
        else:
            return results

    except Exception as e:
        print(e)
        return e 

    finally:
        db.close()


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
    sql = "INSERT INTO user (email, username, password) VALUES (?,?, ?)"
    query_db(sql,(email,username,hashed_password))
    flash("signup sucessful")
    return redirect('/')
 return render_template("signup.html")
 



@app.route( '/login', methods=["GET", "POST"] )
def login():
    print(request.form)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE username = ?"
        user = query_db(sql=sql, args=(username,),one=True)
        if user:
            if check_password_hash(user['password'] ,password):
                session['user'] = user
            flash("logged in sucessfully")
    return render_template('login.html')

@app.route( '/logout')
def logout():
    session['user'] = None
    flash("your logged out")
    return redirect('/')


    
@app.route( '/libary' )
def libary():
        return render_template('libary.html')

@app.route('/Character', methods=("GET","POST"))
def Character():
    print(request.form)
    try:
        user = session['user']
    except KeyError:
        flash("Please log in to continue")
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name'] 
        gender = request.form['gender']
        birthday = request.form['birthday']
        age = request.form['age']
        species = request.form['species'] 
        description = request.form['description']
        backstory = request.form['backstory']
        userId = session['user']['ID']

      
        sql = "INSERT INTO Characters (name, gender, birthday, age, species, description, backstory, user) VALUES (?,?, ?, ?, ?, ?, ?, ?)" 
        query_db(sql,(name, gender, birthday, age, species, description, backstory, userId))
        flash("character added ")
        return redirect('/libary')
    return render_template('Character.html')

@app.route('/Location', methods=("GET","POST"))
def Location():
    print(request.form)
    if request.method == 'POST':
            name = request.form['name'] 
            type = request.form['type']
            description = request.form['description']
            history = request.form['history']
            userId = session["user"]["ID"]
            
            sql = "INSERT INTO Locations (name, type, description, history, userId) VALUES (?,?, ?, ?, ?,)"
            query_db(sql,(name, type, description, history, userId))
            flash("location added ")
    return render_template('location.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(debug=True)
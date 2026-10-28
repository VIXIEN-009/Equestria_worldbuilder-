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

# this  is the route for the home pae of my website and gives the page its own url 
@app.route( '/' )
# this defones the index.html and helps run the home page 
def index():
# renders and returns the hmtl file which means shows the user the home page on their browser 
    return render_template('index.html')

@app.route( '/signup', methods=['GET', 'POST'])
def signup():
 print(request.form)
 if request.method == 'POST':
    email = request.form['email'] 
    username = request.form['username']
    password = request.form['psw']
    #hashes the password when it is entered into the database #
    hashed_password = generate_password_hash(password)
    # this defines the sql stamemenet of putting a new user into the users table 
    sql = "INSERT INTO user (email, username, password) VALUES (?,?, ?)"
    #this here excutes the sql query and sends it to the database 
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
    
    #this if statement checks if the user exists in my database to continue 
        if user:
            
            # checks if the password that is entered is the same as the one in the database 
            if check_password_hash(user['password'] ,password):
               
                #if it matches the user is stored in a session which will stay there till they are loged out 
                session['user'] = user
            flash("logged in sucessfully")
    return render_template('login.html')

@app.route( '/logout')
def logout():
    # this sets the session user to none so the user would have to log in again to get back to session user 
    session['user'] = None
    flash("your logged out")
    return redirect('/')


    
@app.route( '/libary' )
def libary():
        sql = "SELECT * FROM Character WHERE userid  = session['user']['Id']"
        return render_template('libary.html')

@app.route('/Character', methods=("GET","POST"))
def Character():
    print(request.form)
    try:
        user = session['user']
    #this catches the main error and tells the user to log in to continue  
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
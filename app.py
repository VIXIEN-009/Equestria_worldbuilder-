from flask import Flask , render_template
import sqlite3 

app = Flask(__name__)

DATABASE = "database.db"

def query_db(sql,args=(),one=False):
  '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
  db = sqlite3.connect(DATABASE)
  cursor = db.cursor()
  cursor.execute(sql)
  cursor.fetchall()
  db.commit()
  db.close()
  return (results[0] if results else None) if one else results


@app.route( '/' )
def index():
    results = query_db("SELECT * FROM item")  
    return render_template('index.html',results=results)

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
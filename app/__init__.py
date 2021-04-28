#Team hell_os (Jonathan Lee, Dean Carey, Dragos Lup, Ishita Gupta)
#SoftDev 
#P3 -- ArRESTed Development, JuSt in Time
#2021-04-26

from flask import Flask,session         
from flask import render_template
from flask import request, redirect, url_for
from datetime import datetime
import os
import sqlite3
import hashlib
from hashlib import scrypt
import db_builder as dbb # BIG


DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()
username = ''
password = ''

app = Flask(__name__)



# salts and hashes the given string, returns string with 32-char salt appended onto the end
def saltString(string):
    oursalt = os.urandom(32)
    hashedsalted = hashlib.scrypt(string.encode('utf-8'), oursalt, N=16384, r=8, p=1, dklen=32)
    hashedsalted += oursalt
    return hashedsalted

# getting the salt from a string hashed w/ salt by the above method for use in comparisons.
def getHashSalt(string):
    hashsalt = string[:32]

@app.route("/")
def root():
   return render_template('index.html')

@app.route("/login")
def login():

    #simple error check, expand later
    if request.args['username'] == '' or request.args['password'] == '': #Check if fields are filled
        return render_template('error.html', error = 'Some fields are empty, try again') 

    #getting the user
    c = db.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (username))



    session['UserID'] = int(userid[0])
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    # if user is logged in already
    if "username" in session:
        return redirect(url_for('root'))
    


    # checking for existing usernames
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    sameusernames = c.fetchall()
    if len(sameusernames) > 0:
        return render_template('error.html', error = 'A user with that username already exists')
    else:
        dbb.register(username, saltString(password, oursalt), location ) #fix this somehow
        # reminder to get id from the fruitling being added to fruitlings database and add that to the fruits field
        return render_template('register.html')

# epic logout session pop gaming
@app.route("/logout")
def logout():
    session.pop('UserID', None)
    return render_template('login.html')



# -----------------------
# the non-auth parts!!
# -----------------------

def buyfruit(fruitname):
    c = db.cursor()
    c.execute()


if __name__ == "__main__":
    app.debug = True 
    app.run()
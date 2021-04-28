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


app = Flask(__name__)



# salts and hashes the given string, returns string with 32-char salt appended onto the end
def saltStringRandom(string):
    oursalt = os.urandom(32)
    hashedsalted = hashlib.scrypt(string.encode('utf-8'), oursalt, N=16384, r=8, p=1, dklen=32)
    hashedsalted += oursalt
    return hashedsalted

def saltStringExisting(string, salt):
    hashedsalted = hashlib.scrypt(string.encode('utf-8'), salt, N=16384, r=8, p=1, dklen=32)
    hashedsalted += salt
    return hashedsalted

# getting the salt from a string hashed w/ salt by the above method for use in comparisons.
def getHashSalt(string):
    hashsalt = string[:32]
    return hashsalt

@app.route("/")
def root():
   return render_template('index.html')

@app.route("/login")
def login():
    #check if already logged in
    if 'username' in session:
        return render_template('index.html')

    #simple error check (currently empty field check), expand later
    if request.args['username'] == '' or request.args['password'] == '': #Check if fields are filled
        "hi" #insert error handling here

    #first of all, get the username input
    username = request.args['username']

    #Then find the corresponding user info from the db
    c = db.cursor() 
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    data = c.fetchall()[0] #whew. only one. of em.

    #get salt from the password and hash+salt password
    password = saltStringExisting(request.args['password'], getHashSalt(data[2]))

    #compare hash+salt pws, if they match, start session
    if password == data[2]:
        print(data[0]) #just printing the user id :flushed:
        session['ID'] = int(data[0])
        session['username'] = data[1]

        return render_template('index.html') #make sure to add index html changing with stuff in session

    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    # if user is logged in already
    if "username" in session:
        return render_template('index.html')
        # bother with the line below later
        # return redirect(url_for('root'))

    # checking for existing usernames
    username = request.args['username']
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    sameusernames = c.fetchall()
    if len(sameusernames) > 0:
        return render_template('error.html', error = 'A user with that username already exists')
    
    #if there isn't a dupe user, move on to the actual meat.
    else:
        #getting the user's id to use with the new fruit
        c.execute('SELECT MAX(id) FROM users')
        newid = c.fetchall() + 1

        #registering the fruit
        dbb.new_fruit(newid, request.args['fruit'])

        #getting the fruit's id to use with the new user
        c.execute('SELECT MAX(fruit_id) FROM fruitlings')
        fruitid = c.fetchall()
        
        #registering the user
        dbb.register(username, saltStringRandom(request.args['password']), request.args['location'], str(fruitid) + ",")

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
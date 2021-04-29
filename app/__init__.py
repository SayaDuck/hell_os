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
import app.db_builder as dbb # BIG


DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()


app = Flask(__name__)



# salts and hashes the given string, returns string with 32-char salt appended onto the end
def saltStringRandom(string):
    oursalt = os.urandom(32)
    hashedsalted = hashlib.pbkdf2_hmac('sha256', bytes(str(string), encoding='utf8'), oursalt, 100000)
    hashedsalted += oursalt
    print(hashedsalted)
    return str(hashedsalted)

def saltStringExisting(string, salt):
    hashedsalted = hashlib.pbkdf2_hmac('sha256', bytes(string, encoding='utf8'), bytes(salt, encoding='utf8'), 100000)
    hashedsalted += bytes(salt, encoding='utf8')
    print(hashedsalted)
    return str(hashedsalted)

# getting the salt from a string hashed w/ salt by the above method for use in comparisons.
def getHashSalt(string):
    hashsalt = string[:32]
    return hashsalt


@app.route("/")  #make sure to add root changing with stuff in session
def root():
    if 'username' in session:
        return render_template('index.html', user = session.get['username'])
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():

    #check if already logged in
    if 'username' in session:
        return redirect(url_for('root'))

    if "login" in request.form:
        
        #simple error check (currently empty field check), expand later
        if (request.form['inputusername'] == '' or request.form['inputpassword'] == ''): #Check if fields are filled
            "hi" #insert error handling here

        if dbb.checkUsername(request.form['inputusername']):
            #get salt from the password and hash+salt password
            password = saltStringExisting(request.form['inputpassword'], getHashSalt(dbb.getInfo(request.form['inputusername'],'password')))

            #compare hash+salt pws, if they match, start session
            if str(password) == str(dbb.getInfo(request.form['inputusername'],'password')): # yoo correct password?!
                print(dbb.getInfo(request.form['inputusername'],'id')) #just printing the user id :flushed:
                session['ID'] = int(dbb.getInfo(request.form['inputusername'],'id'))
                session['username'] = request.form['inputusername']
                print(session['username']) #diagnostic print
                return redirect(url_for('root'))
        
            else: # yoo incorrect password >:(
                return redirect(url_for('login')) #add error to this later
        else:
            return render_template('login.html')
            #add error: username doesn't exist

    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    # if user is logged in already
    if "username" in session:
        return redirect(url_for('root'))   

    if "register" in request.form:
        #print(request.form)

        if (request.form['inputusername'] == '' or request.form['inputpassword'] == ''):
            "fields blank error"

        else:
            if dbb.checkUsername(request.form['inputusername']):
                "user already exists error"
            #if there isn't a dupe user, move on to the actual meat.
            else:            
                #registering the user
                dbb.register(request.form['inputusername'], saltStringRandom(request.form['inputpassword']), request.form['location'], "")
                
                #registering the fruit
                dbb.new_fruit(dbb.getInfo(request.form['inputusername'], id), request.form['fruit'])


                return redirect(url_for('login'))

    #without submission of form
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
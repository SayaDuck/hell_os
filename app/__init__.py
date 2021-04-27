#Team hell_os (Jonathan Lee, Dean Carey, Dragos Lup, Ishita Gupta)
#SoftDev 
#P3 -- ArRESTed Development, JuSt in Time
#2021-04-26

from flask import Flask,session         
from flask import render_template
from flask import request, redirect
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)

# @app.route("/")
# def root():
#     return render_template('')

app.route("/login")
def login():

    return render_template('login.html')

app.route("/register")
def register():

    return render_template('register.html')




if __name__ == "__main__":
    app.debug = True 
    app.run()
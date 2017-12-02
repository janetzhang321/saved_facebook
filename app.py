from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash, jsonify
import json, os, urllib, hashlib
from time import gmtime, strftime

app = Flask(__name__)

app.secret_key = 'idk'#os.urandom(32)
secret=""

'''
mockup of facebook newsfeed page
'''
@app.route("/", methods=["GET","POST"])
def main():
    #if(secret in session):

    return render_template("index.html")

'''
DEBUG and RUN
'''


if __name__ == '__main__':
    app.debug=True
    app.run(threaded=True)

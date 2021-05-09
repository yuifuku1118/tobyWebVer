# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from toby import main

app = Flask(__name__)

# Routing
@app.route('/')
def index():
    title = "ようこそ"
    return render_template('index.html',
                           message="Hi tell me anything you want!", title=title)

@app.route('/post', methods=['POST', 'GET'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        text = request.form['name']
        reply,score, scorelist = main(text)
        print(reply)
        return render_template('index.html',
                               name=reply, score = score, listS = scorelist, title=title)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
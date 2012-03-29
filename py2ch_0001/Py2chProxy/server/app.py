# -*- coding: utf-8 -*-

from Py2chProxy.core import util
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
  p = {}
  return render_template("index.html")

@app.route('/<server>/<board>/<id>/')
def thread(server, board, id):
  if "X-PJAX" in request.headers and query:
    return render_template("thread-pjax.html", p=p)
  else:
    
    return render_template("thread.html", p=p)


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=8888)


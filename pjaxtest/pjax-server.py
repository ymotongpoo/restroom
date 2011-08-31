# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
  p = {}
  return render_template("index.html", p=p)

@app.route('/pjax/<query>')
def pjax_index(query):
  p = {}
  if "X-PJAX" in request.headers and query:
    return "you requested '%s' in pjax" % query
  else:
    p['placeholder'] = "you requested '%s' in static" % query
    return render_template("index.html", p=p, )

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8888)
  


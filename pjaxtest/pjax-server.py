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
    content = "you requested '%s' in pjax" % query
    p['placeholder'] = content
    return render_template("container.html", p=p)
  else:
    p['placeholder'] = "you requested '%s' in static" % query
    p['static'] = True
    return render_template("index.html", p=p)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8888)
  


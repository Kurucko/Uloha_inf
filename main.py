from flask import Flask, render_template, url_for, request, jsonify
import math
from PIL import Image, ImageColor
import os

app = Flask(__name__)



@app.route("/")
def hello():
    return render_template("index.html")

# @app.route("/")
@app.route("/", methods=["POST"])
def save_data():
    
    data = request.form["data"]
    w = request.form["w"]
    n = int(request.form["n"])
    my_var = data
    
    
    my_var += "\n"
    my_var = my_var.split("\n")
    
    sprava, img = rasterizacia(my_var,w)
    if os.path.exists(f"static/canvas.png"):
        os.remove(f"static/canvas.png")
    if img != "":
        img.save(f"static/canvas.png")
    
    print("ok")
    return jsonify(sprava, os.path.exists(f"static/canvas.png"))

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///lehtinen.db")

list = ["firstname", "lastname", "email", "filename", "filepath", "filetype", "date", "mouse", "bath", "injection", "length", "time", "framerate", "frames", "response", "notes"]
list2 = ["firstname1", "lastname1", "email1", "filename1", "filepath1", "filetype1", "date1", "mouse1", "bath1", "injection1", "length1", "time1", "framerate1", "frames1", "response1", "notes1"]

@app.route("/")
def homepage():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/enter", methods=["GET", "POST"])
def input():
    if request.method == "GET":
        return render_template("enter.html")
    else:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        filename = request.form.get("filename")
        filepath = request.form.get("filepath")
        filetype = request.form.get("filetype")
        ifother = request.form.get("ifother")
        date = request.form.get("date")
        mouse = request.form.get("mouse")
        bath = request.form.get("bath")
        injection = request.form.get("injection")
        length = request.form.get("length")
        time = request.form.get("time")
        framerate = request.form.get("framerate")
        frames = request.form.get("frames")
        response = request.form.get("response")
        notes = request.form.get("notes")

        if framerate == None and frames != None and length != None:
            framerate = round(frames / float(length))
        if frames == None and framerate != None and length != None:
            frames = round(framerate * float(length))
        if length == None and frames != None and framerate != None:
            length = str(float(frames)/framerate)
        if filetype == "OTHER":
            filetype == ifother

        db.execute("INSERT INTO experiments (firstname, lastname, email, filename, filepath, filetype, ifother, date, mouse, bath, injection, length, time, framerate, frames, response, notes) VALUES (:fn, :ln, :em, :fin, :fip, :fit, :io, :da, :mo, :ba, :inj, :le, :ti, :frr, :fr, :re, :no)",
                    fn=firstname, ln=lastname, em=email, fin=filename, fip=filepath, fit=filetype, io=ifother, da=date, mo=mouse, ba=bath, inj=injection, le=length, ti=time, frr=framerate, fr=frames, re=response, no=notes)

        return redirect("/")

query = {}
@app.route("/request", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        return render_template("request.html")
    else:
        values = {}
        for i in range(len(list)):
            val = request.form.get(list[i])
            values[list[i]] = val
        for key in values:
            if values[key] != None:
                query.update( {key : values[key]} )
        return render_template("request2.html", query=query)

@app.route("/request2", methods=["GET", "POST"])
def ask2():
    if request.method == "GET":
        return render_template("request2.html")
    else:
        strings1 = []
        for q in query:
            new = request.form.get(q)
            if not request.form.get(q):
                return render_template("sorry.html")
            string = '{} LIKE "{}"'. format(q, new)
            strings1.append(string)
        cond_string = ""
        for s in range(len(strings1)):
            cond_string += strings1[s]
            if s < len(strings1) -1:
                cond_string += " AND "
        values = {}
        output = []
        titles = []
        for i in range(len(list2)):
            val = request.form.get(list2[i])
            values[list2[i]] = val
        for key in values:
            if values[key] != None:
                output.append(key)
                titles.append(values[key])
        select_string = ""
        for o in range(len(output)):
            select_string += output[o][:-1]
            if o < len(output) - 1:
                select_string += ", "
        if select_string == "":
            select_string = "*"
        query_string = "SELECT " + select_string + " FROM experiments WHERE " + cond_string
        rows = db.execute(query_string)
        query.clear()
        #return render_template("test.html", rows = rows)
        return render_template("data.html", rows = rows)



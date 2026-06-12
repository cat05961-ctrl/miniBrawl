
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "change_me"

USER="admin"
PASS="admin123"

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("username")==USER and request.form.get("password")==PASS:
            session["ok"]=True
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("ok"):
        return redirect("/")
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

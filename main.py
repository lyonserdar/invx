from flask import (
    Flask, 
    redirect, 
    url_for, 
    render_template,  
    request, 
    session, 
    flash, 
    send_from_directory
)
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "very_secret_key"
app.permanent_session_lifetime = timedelta(days=30)


# Path for the main Svelte page
@app.route("/")
def index():
    return  send_from_directory("client/public", "index.html")


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory("client/public", path)


@app.route("/rand")
def hello():
    return str(random.randint(0, 100))


@app.get("/login")
@app.post("/login")
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user
        return redirect(url_for("get_user"))
    else:  
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.get("/user")
def get_user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))
    

@app.get("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
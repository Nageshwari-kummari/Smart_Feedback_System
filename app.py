from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# temporary storage
users = []
feedbacks = []

# admin credentials
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users.append({
            "email": request.form["email"],
            "password": request.form["password"]
        })
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        for u in users:
            if u["email"] == request.form["email"] and u["password"] == request.form["password"]:
                session["user"] = u["email"]
                return redirect("/welcome")
    return render_template("login.html")


@app.route("/welcome")
def welcome():
    if "user" not in session:
        return redirect("/login")
    return render_template("welcome.html")


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        feedbacks.append({
            "rating": int(request.form["rating"]),
            "comment": request.form["comment"]
        })
        return redirect("/thankyou")

    return render_template("feedback.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["email"] == ADMIN_EMAIL and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin/dashboard")
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    ratings = [f["rating"] for f in feedbacks]
    comments = [f["comment"] for f in feedbacks]

    return render_template("admin_dashboard.html",ratings=ratings,comments=comments)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from db import engine, Users

app = Flask(__name__, template_folder="../template", static_folder="../static")


# a home/main page for sign-up, login and other stuff
# a api with databse that update as user updates
# it shoudl returns as json


@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/main")
def main():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        data = request.get_json()
        user_password = data.get("password")
        username = data.get("username")
        with Session(engine) as session:
            user = session.execute(
                select(Users).where(Users.username == data.get("username"))
            ).scalar_one_or_none()
        if not user or user.password != user_password:
            return jsonify({"error": "username or password error"}), 200

        return jsonify({"message": "Login success", "username": username}), 200


@app.route("/register", methods=["GET", "POST"])
def signIn():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        if not username or not data.get("password"):
            return jsonify({"Error": "Missing Fields"}), 400
        # check if user already exists
        # loop though the whole databse
        with Session(engine) as session:
            users = session.execute(
                select(Users).where(Users.username == data.get("username"))
            ).scalar_one_or_none()
            if users:
                return jsonify({"error": "users exists"})
            # add to database
            session.add(Users(username=data["username"], password=data["password"]))
            session.commit()
            return jsonify({"username": username}), 200


if __name__ == "__main__":
    app.run(port=4000)

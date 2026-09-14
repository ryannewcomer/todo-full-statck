from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import Session as DBSession
from db import engine, Users, Tasks

app = Flask(__name__, template_folder="../template", static_folder="../static")


# a home/main page for sign-up, login and other stuff
# a api with databse that update as user updates
# it shoudl returns as json
app.secret_key = secrets.token_hex()


# select all tasks from Tasks, set as var, pass to tempalte
@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/main")
# get task and dueDays from Tasks and display on the html
def main():

    with DBSession(engine) as sessions:
        all_tasks = (
            sessions.execute(select(Tasks).where(Tasks.user_id == session["user_id"]))
            .scalars()
            .all()
        )
    return render_template("home.html", tasks=all_tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        data = request.get_json()
        user_password = data.get("password")
        username = data.get("username")
        with DBSession(engine) as sessions:
            user = sessions.execute(
                select(Users).where(Users.username == data.get("username"))
            ).scalar_one_or_none()
            session["user_id"] = user.id
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
        with DBSession(engine) as sessions:
            users = sessions.execute(
                select(Users).where(Users.username == data.get("username"))
            ).scalar_one_or_none()

            session["user_id"] = users.id
            if users:
                return jsonify({"error": "users exists"})
            # add to database
            sessions.add(Users(username=data["username"], password=data["password"]))
            sessions.commit()
            return jsonify({"username": username}), 200


# tasks
@app.route("/add", methods=["GET", "POST"])
def addTasks():
    if request.method == "GET":
        return render_template("addTasks.html")
    if request.method == "POST":
        data = request.get_json()
        user_id = session.get("user_id")
        user_desc = data.get("desc")
        user_date = data.get("date")
        if not user_id or not user_desc:
            return jsonify({"error": "Missing data"}), 400

        with DBSession(engine) as db_session:
            db_session.add(Tasks(desc=user_desc, dueDays=user_date, user_id=user_id))
            tasks_id = db_session.execute(
                select(Tasks.id).where(
                    Tasks.desc == user_desc,
                    Tasks.dueDays == user_date,
                    Tasks.user_id == user_id,
                )
            )
            db_session.commit()
        return jsonify({"message": "tasks added"}), 201


# find a way to get the task id from the main page for that task
# delete it from the db
# update main apage again
@app.route("/delete", methods=["POST"])
def deleteTasks():
    data = request.get_json()
    task_id = data.get("task_id")
    if not task_id:
        return jsonify({"error": "missing data"}), 400
    with DBSession(engine) as db_session:
        db_session.execute(delete(Tasks).where(Tasks.id == task_id))
        db_session.commit()
    return jsonify({"message": "tasks deleted"}), 201


# edit tasks


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def editTasks(task_id):
    print("EDIT FUNC CALL")
    print(f"Method: {request.method}")
    print(f"Content-Type header: {request.headers.get('Content-Type')}")
    print(f"Request data: {request.data}")

    if request.method == "GET":
        print("GET RUNNS NOW")
        with DBSession(engine) as sessions:
            task = sessions.execute(
                select(Tasks).where(Tasks.id == task_id)
            ).scalar_one_or_none()
        return render_template("editTasks.html", task=task)

    if request.method == "POST":
        print("POST RUNNES NOW")
        try:
            print("Attempting to get JSON")
            data = request.get_json()
            print(f"JSON data received: {data}")

            if not data:
                print("ERROR: No JSON data")
                return jsonify({"error": "Missing data"}), 400

            with DBSession(engine) as db_session:
                stmt = (
                    update(Tasks)
                    .where(Tasks.id == task_id)
                    .values(desc=data.get("desc"), dueDays=data.get("dueDays"))
                )
                db_session.execute(stmt)
                db_session.commit()
                print("Database updated successfully")

            return jsonify({"message": "Task updated"}), 200
        except Exception as e:
            print(f"ERROR in POST handler: {e}")
            import traceback

            traceback.print_exc()
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=4000)

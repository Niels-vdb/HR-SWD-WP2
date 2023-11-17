import os.path

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt

import sqlite3

from lib.query_model import QuerylModel

from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database

# from lib.forms import LoginForm, SubmitForm

# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.config["SECRET_KEY"] = "ThisIsTheBiggestSecretEver"
bcrypt = Bcrypt(app)

# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, "databases", "testcorrect_vragen.db")

query_model = QuerylModel(DATABASE_FILE)

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)


# Checks if you are logged in
@app.before_request
def check_login():
    if request.endpoint not in ["static", "login", "handle_login"]:
        if not session.get("logged_in"):
            return redirect(url_for("login"))


# Login screen
@app.route("/")
def login():
    return render_template("login.html")


# Login handler
@app.route("/handle_login", methods=["POST"])
def handle_login():
    session["admin"] = False

    for tuple in query_model.get_first_name(request.form["login-email"]):
        for name in tuple:
            session["name"] = name

    for tuple in query_model.get_full_name(request.form["login-email"]):
        full_name = []

        for name in tuple:
            full_name.append(name)

        name = " ".join(full_name)

        session["full_name"] = name

    for tuple in query_model.get_user_id(request.form["login-email"]):
        for id in tuple:
            session["user_id"] = id

    if query_model.password_check(request.form["login-email"]) == None:
        redirect(url_for("login"))
        flash("Email bestaat niet")
    else:
        for password in query_model.password_check(request.form["login-email"]):
            if bcrypt.check_password_hash(password[0], request.form["login-password"]):
                session["logged_in"] = True
                print('logged in')
            else:
                flash("Verkeerd wachtwoord")

    for tuple in query_model.admin_check(request.form["login-email"]):
        for data in tuple:
            if data == 1:
                session["admin"] = True

    return redirect(url_for("menu"))


# Log off handler
@app.route("/handle_log_off", methods=["POST"])
def handle_log_off():
    session["logged_in"] = False
    return redirect(url_for("login"))


# Maybe get the users name to print on screen
@app.route("/menu")
def menu():
    return render_template("menu.html")


# Screen for altering questions
@app.route("/edit_questions")
def edit_questions():
    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
    }

    return render_template("edit-questions.html", quark=quark)


# Save altered questions
@app.route("/save_leerdoel/<question_id>", methods=["POST"])
def save_leerdoel(question_id):
    query_model.save_leerdoel(question_id, request.form["leerdoel"], session["user_id"])

    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
    }

    return render_template("edit-questions.html", quark=quark)


@app.route("/save_author/<question_id>", methods=["POST"])
def save_author(question_id):
    query_model.save_author(question_id, request.form["author"], session["user_id"])
    author_trigger = False

    if request.form["edit-bad-authors"] == "True":
        author_trigger = True

    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
        "author_trigger": author_trigger,
    }

    return render_template("edit-questions.html", quark=quark)


@app.route("/save_question/<question_id>", methods=["POST"])
def save_question(question_id):
    query_model.save_question(question_id, request.form["question"], session["user_id"])
    question_trigger = False

    if request.form["edit-bad-sys-code"] == "True":
        question_trigger = True

    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
        "question_trigger": question_trigger,
    }

    return render_template("edit-questions.html", quark=quark)


# Reset changed question
@app.route("/reset_question", methods=["POST"])
def reset_question():
    question_trigger = False

    if request.form["edit-bad-sys-code"] == "True":
        question_trigger = True

    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
        "question_trigger": question_trigger,
    }

    return render_template("edit-questions.html", quark=quark)


# Save question as exception
@app.route("/leerdoel_exception/<question_id>", methods=["POST"])
def leerdoel_exception(question_id):
    query_model.leerdoel_exception(question_id, session["user_id"])

    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
    }

    return render_template("edit-questions.html", quark=quark)


@app.route("/author_exception/<question_id>", methods=["POST"])
def author_exception(question_id):
    query_model.author_exception(question_id, session["user_id"])
    author_trigger = False

    if request.form["edit-bad-authors"] == "True":
        author_trigger = True

    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
        "author_trigger": author_trigger,
    }

    return render_template("edit-questions.html", quark=quark)


@app.route("/sys_code_exception/<question_id>", methods=["POST"])
def sys_code_exception(question_id):
    query_model.sys_code_exception(question_id, session["user_id"])
    question_trigger = False

    if request.form["edit-bad-sys-code"] == "True":
        question_trigger = True

    quark = {
        "leerdoel_questions": query_model.get_questions_without_leerdoel(),
        "author_questions": query_model.get_questions_without_author(),
        "system_code_questions": query_model.questions_with_bad_syntax(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
        "question_trigger": question_trigger,
    }

    return render_template("edit-questions.html", quark=quark)


# Screen to see question exceptions
@app.route("/question_exceptions")
def question_exceptions():
    quark = {
        "exceptions": query_model.get_all_question_exceptions(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
    }

    return render_template("question-exceptions.html", quark=quark)


# Handles question exception restore
@app.route("/restore_question_exception/<question_id>", methods=["POST"])
def restore_question_exception(question_id):
    query_model.restore_question_exception(question_id)
    return redirect(url_for("question_exceptions"))


# Screen for altering authors
@app.route("/edit_authors")
def edit_authors():
    quark = {
        "employee_authors": query_model.get_bad_employee_tabels(),
        "birth_year_authors": query_model.get_bad_author_birthdate_tabels(),
    }

    return render_template("edit-authors.html", quark=quark)


# Save altered author
@app.route("/save_employee/<author_id>", methods=["POST"])
def save_employee(author_id):
    query_model.save_employee(author_id, session["user_id"])
    employee_trigger = False

    if request.form["edit-bad-employee"] == "True":
        employee_trigger = True

    quark = {
        "employee_authors": query_model.get_bad_employee_tabels(),
        "birth_year_authors": query_model.get_bad_author_birthdate_tabels(),
        "employee_trigger": employee_trigger,
    }

    return render_template("edit-authors.html", quark=quark)


@app.route("/save_non_employee/<author_id>", methods=["POST"])
def save_non_employee(author_id):
    query_model.save_non_employee(author_id, session["user_id"])
    employee_trigger = False

    if request.form["edit-bad-employee"] == "True":
        employee_trigger = True

    quark = {
        "employee_authors": query_model.get_bad_employee_tabels(),
        "birth_year_authors": query_model.get_bad_author_birthdate_tabels(),
        "employee_trigger": employee_trigger,
    }

    return render_template("edit-authors.html", quark=quark)


@app.route("/save_new_birth_year/<author_id>", methods=["POST"])
def save_birth_year(author_id):
    query_model.save_birth_year(
        author_id, request.form["new-birth-year"], session["user_id"]
    )
    return redirect(url_for("edit_authors"))


# Save question as exception
@app.route("/employee_exception/<question_id>", methods=["POST"])
def employee_exception(question_id):
    query_model.employee_exception(question_id, session["user_id"])

    employee_trigger = False
    if request.form["edit-bad-employee"] == "True":
        employee_trigger = True

    quark = {
        "employee_authors": query_model.get_bad_employee_tabels(),
        "birth_year_authors": query_model.get_bad_author_birthdate_tabels(),
        "employee_trigger": employee_trigger,
    }

    return render_template("edit-authors.html", quark=quark)


@app.route("/birth_year_exception/<question_id>", methods=["POST"])
def birth_year_exception(question_id):
    query_model.birth_year_exception(question_id, session["user_id"])
    return redirect(url_for("edit_authors"))


# Screen to see author exceptions
@app.route("/author_exceptions")
def author_exceptions():
    quark = {
        "exceptions": query_model.get_all_author_exceptions(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
    }

    return render_template("author-exceptions.html", quark=quark)


# Handles author exception restore
@app.route("/restore_author_exception/<author_id>", methods=["POST"])
def restore_author_exception(author_id):
    query_model.restore_author_exception(author_id)
    return redirect(url_for("author_exceptions"))


# Screen for filtering database
@app.route("/filter")
def filter():
    quark = {
        "question_table": query_model.get_all_questions(),
        "leerdoelen": query_model.get_leerdoelen(),
        "authors": query_model.get_authors(),
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
        "users": query_model.get_users(),
    }

    return render_template("filter.html", quark=quark)


# Screen for filtered data
@app.route("/filtered_data", methods=["POST"])
def filtered_data():
    quark = {
        "filtered": [],
        "single_leerdoel": query_model.get_leerdoel_table(),
        "single_author": query_model.get_auteur_table(),
        "single_user": query_model.get_single_users(),
    }

    option = request.form.getlist("filter-radio")
    print(option)

    if "uid-radio" in option:
        quark["filtered"] = query_model.uid_filter(
            request.form["uid-min"], request.form["uid-max"]
        )

    if "leerdoel-radio" in option:
        quark["filtered"] = query_model.leerdoel_filter(option.pop())
    if "faulty-leerdoel-radio" in option:
        quark["filtered"] = query_model.faulty_leerdoel()

    if "author-radio" in option:
        quark["filtered"] = query_model.author_filter(option.pop())
    if "faulty-author-radio" in option:
        quark["filtered"] = query_model.faulty_author()

    if "int-employee-radio" in option:
        quark["filtered"] = query_model.int_employee()
    if "ext-employee-radio" in option:
        quark["filtered"] = query_model.ext_employee()
    if "faulty-employee-radio" in option:
        quark["filtered"] = query_model.faulty_employee()

    if "leerdoel-exc-radio" in option:
        quark["filtered"] = query_model.filter_leerdoel_exceptions()
    if "author-exc-radio" in option:
        quark["filtered"] = query_model.filter_author_exceptions()
    if "sys-code-exc-radio" in option:
        quark["filtered"] = query_model.filter_sys_code_exceptions()

    if "changed-by-user" in option:
        query_model.filter_changed_by_user(option.pop())
        quark["filtered"] = query_model.filter_changed_by_user(option.pop())
    if "exception-by-user" in option:
        quark["filtered"] = query_model.filter_exception_by_user(option.pop())

    # return filtered
    return render_template("filtered.html", quark=quark)


# Screen to make new user
@app.route("/new_user")
def new_user():
    return render_template("new-user.html")


# Handles new user
@app.route("/create_new_user", methods=["POST"])
def create_new_user():
    password = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
    try:
        if request.form.getlist("admin"):
            query_model.set_new_user(
                request.form["first-name"],
                request.form["infix"],
                request.form["last-name"],
                request.form["email"],
                password,
                True,
            )
            flash("Admin gebruiker aangemaakt")
        else:
            query_model.set_new_user(
                request.form["first-name"],
                request.form["infix"],
                request.form["last-name"],
                request.form["email"],
                password,
                False,
            )
            flash("Gebruiker aangemaakt")
    except sqlite3.IntegrityError:
        flash("Gebruiker bestaat al")
    # Functionality for existing email

    return redirect(url_for("new_user"))


# Screen with all users
@app.route("/see_users")
def see_users():
    users = query_model.get_users()
    return render_template("see_users.html", users=users)


# Handles user delete
@app.route("/delete_user/<user_id>", methods=["POST"])
def delete_user(user_id):
    query_model.delete_user(user_id)
    return redirect(url_for("see_users"))


@app.route("/tryout")
def tryout():
    # questions = query_model.faulty_leerdoel()
    return render_template("tryout.html")


@app.route("/database")
def databases():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )


if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)

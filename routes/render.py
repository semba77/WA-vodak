from flask import Flask, Blueprint, render_template, request, redirect, url_for, make_response
from extensions import connect
from database.user import User
from database.baseTable import BaseTable, NoResultsFoundException
from decorators import only_auth

render_blueprint = Blueprint(
    "render",
    __name__,
    url_prefix="/"
)

def get_login():
    return render_template('login.html',**{
        "error_message": request.args.get("error_message", None)
    })
render_blueprint.add_url_rule("login/","get_login",get_login,methods=["GET"])

def post_login():
    redirect_page:str = request.args.get("redirect_page", None)
    form_username: str = request.form["username"]
    form_password: str = request.form["password"]
    try:
        user = User.read_one_username(connect(), form_username)
    except NoResultsFoundException as e:
        return redirect(url_for('render.get_login', redirect_page=redirect_page, error_message="Špatné uživatelské jméno"))
    print(str(user))
    if user.password == form_password:
        if not redirect_page is None:
            response = make_response(redirect(redirect_page))
        else:
            print("redirect index")
            response = make_response(redirect(url_for("render.index")))
            print(url_for("render.index"))
        response.set_cookie("user_id",str(user.id))
        return response
    return redirect(url_for('render.get_login', redirect_page=redirect_page, error_message="Špatné heslo"))
render_blueprint.add_url_rule("login/","post_login",post_login,methods=["POST"])

@only_auth()
def get_logout():
    response = make_response(redirect(url_for("render.get_login")))
    response.delete_cookie("user_id")
    return response
render_blueprint.add_url_rule("logout/","get_logout",get_logout,methods=["GET"])

@only_auth()
def index():
    return render_template("prvni_stranka.html")
render_blueprint.add_url_rule("","index",index,methods=["GET"])

@only_auth()
def register():
    return render_template("register.html")
render_blueprint.add_url_rule("registrace/","register", register, methods=["GET"])

def show():
    return render_template('show.html')
render_blueprint.add_url_rule("show/","show", show, methods=["GET"])
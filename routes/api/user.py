from flask import Flask, Blueprint, render_template, request, jsonify
import re
from decorators import api_only_auth
from database.register import Register
from database.user import User
from database.baseTable import NoResultsFoundException
from extensions import connect

user_blueprint = Blueprint(
    "user",
    __name__,
    url_prefix="/user/"    
)

@api_only_auth()
def get():
    user_id: int = int(request.headers.get("user-id",0))
    try:
        username: str = User.read_one_by_atributes(connect(), id=user_id).username
        return jsonify({
            "username": username    
        }), 200
    except NoResultsFoundException as e:
        return jsonify({

        }), 400
user_blueprint.add_url_rule('','get', get, methods=["GET"])

@api_only_auth()
def get_username(user_id):
    user_id: int = int(user_id)
    print(user_id)
    try:
        user: User = User.read_one_by_atributes(connect(), id=user_id)
        return jsonify({
            "username": user.username,
            "finish": user.finish,
            "canSwim": user.can_swim   
        }), 200
    except NoResultsFoundException as e:
        return jsonify({

        }), 400
    except BaseException as e:
        print(type(e), " ==> ",e)
        return jsonify({})
user_blueprint.add_url_rule('<int:user_id>/','get_username', get_username, methods=["GET"])

@api_only_auth()
def get_my_requests():
    user_id: int = int(request.headers.get("user-id",0))
    requests = Register.read_many_by_atributes(connect(), user2_id=user_id)
    return jsonify({
        "requests":[tmp.__dict__() for tmp in requests]
    }), 200
user_blueprint.add_url_rule('my_requests/','get_my_requests', get_my_requests, methods=["GET"])

@api_only_auth()
def post_result_of_request():
    print('debug')
    data = dict(request.get_json())
    sender = int(data["sender"])
    reciever = int(data["reciever"])
    print('valid confirm start')
    register = Register.read_one_by_atributes(connect(), user_id=reciever,user2_id=sender)
    print('valid confirm 1')
    Register.update(connect(), register.id, user2_decision=True)
    print('valid confirm 2')
    User.update(connect(),sender, finish=True)
    print('valid confirm 3')
    User.update(connect(),reciever, finish=True)
    print('valid confirm end')
    return jsonify({"debug":True})
user_blueprint.add_url_rule('result/','post_result_of_request', post_result_of_request, methods=["POST"])

@api_only_auth()
def idkUz():
    data = dict(request.get_json())
    cs = int(data["canSwim"])
    user_id = int(data["user"])
    User.update(connect(), user_id, canSwim=cs)
    return jsonify({}), 200
user_blueprint.add_url_rule('canSwim/','canSwim', idkUz, methods=["POST"])
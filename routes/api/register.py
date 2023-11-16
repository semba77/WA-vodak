from flask import Flask, Blueprint, render_template, request, jsonify
import re
from decorators import api_only_auth
from database.register import Register
from database.user import User
from database.baseTable import NoResultsFoundException
from extensions import connect

register_blueprint = Blueprint(
    "register",
    __name__,
    url_prefix="/register/"    
)

@api_only_auth()
def post():
    data = request.json
    nickname = data.get("nick",None)
    is_swimming = data.get("je_plavec", None)
    friend = data.get("kanoe_kamarad",None)
    
    owner_user: User = User.read_one_by_atributes(connect(), id=request.headers.get('user-id', None))
    friend_user: User = User.read_one_by_atributes(connect(), username=friend)
    
    pattern = re.compile("^[a-zA-Z0-9]{2,20}$")
    if not bool(pattern.match(nickname)):
        return jsonify({
            "meta":{
                
            }    
        }), 400
    if not type(is_swimming) == bool:
        return jsonify({
            "meta":{
                
            }    
        }), 400
    if not is_swimming:
        return jsonify({
            "meta":{
                
            }    
        }), 400
    User.update(connect(), owner_user.id, canSwim=True)
    try:
        register = Register.read_one_by_atributes(connect(), user_id=owner_user.id)
        Register.update(connect(), register.id, is_swimming=is_swimming, user2_id=friend_user.id, user2_decision=None)
        return jsonify({
        
        }), 201
    except NoResultsFoundException as e:
        print('no result')
        register_id = Register.create(connect(), user_id=owner_user.id, is_swimming=is_swimming, user2_id=friend_user.id, user2_decision=None)
        return jsonify({
            "debug":register_id
        }), 201
register_blueprint.add_url_rule("","post", post, methods=["POST"])

def get_all_finished_registrations():
    tmp: Register = Register.read_many_by_atributes(connect(), user2_decision=True)
    temp = []
    for i in tmp:
        user1 = User.read_one_id(connect(), i.user_id)
        user2 = User.read_one_id(connect(), i.user2_id)
        temp.append({
            "u1":user1.username,
            "u2":user2.username
        })
    return jsonify(temp);
register_blueprint.add_url_rule("allFinished/","idk", get_all_finished_registrations, methods=["GET"])
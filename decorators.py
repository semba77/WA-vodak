from flask import request, session
from flask import Flask, request, redirect, url_for, jsonify

def only_auth(groups=[], redirect_page=None):
    def decorator(view_func):
        def wrapper_func(*args, **kwargs):
            user_id = request.cookies.get('user_id',None)
            if user_id is None:
                return redirect(url_for('render.get_login', redirect_page=request.path))
            return view_func(*args, **kwargs)
        return wrapper_func
    return decorator

def api_only_auth(groups=[], redirect_page=None):
    def decorator(view_func):
        def wrapper_func(*args, **kwargs):
            user_id = request.headers.get('user-id',None)
            if user_id is None:
                return jsonify({
                    "meta":{
                        "code":401,
                        "status":"ER",
                        "message_id":"0001",
                        "atribute":"user_id"
                    }
                }), 401
            return view_func(*args, **kwargs)
        return wrapper_func
    return decorator
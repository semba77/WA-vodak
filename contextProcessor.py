from flask import request, g

def is_auth():
    def func():
        user_id = request.cookies.get('user_id',None)
        return user_id is not None
    return dict(is_auth=func)
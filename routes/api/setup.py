from flask import Flask, Blueprint, render_template, request, jsonify
import re
from decorators import api_only_auth
from routes.api.register import register_blueprint
from routes.api.user import user_blueprint

api_blueprint = Blueprint(
    "api",
    __name__,
    url_prefix="/api/"    
)

api_blueprint.register_blueprint(register_blueprint)
api_blueprint.register_blueprint(user_blueprint)
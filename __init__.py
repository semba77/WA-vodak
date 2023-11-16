from flask import Flask
from routes.render import render_blueprint
from routes.api.setup import api_blueprint
import contextProcessor


app = Flask(__name__)

app.register_blueprint(render_blueprint)
app.register_blueprint(api_blueprint)

app.context_processor(contextProcessor.is_auth)

app.run(host="0.0.0.0",
        port=8000,
        debug=True)

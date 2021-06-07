from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from tasks import api as tasks_api

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version="1.0",
    title="TodoMVC API",
    description="A simple TodoMVC API",
)
api.add_namespace(tasks_api)


if __name__ == "__main__":
    app.run(debug=True)

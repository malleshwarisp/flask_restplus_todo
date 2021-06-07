from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from db import close_db
from tasks import api as tasks_api
from users import api as users_api

authorizations = {
    "Basic Auth": {"type": "basic", "in": "header", "name": "Authorization"},
}

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version="1.0",
    title="TodoMVC API",
    description="A simple TodoMVC API",
    authorizations=authorizations,
)
api.add_namespace(tasks_api)
api.add_namespace(users_api)


@app.teardown_appcontext
def close_connection(exception):
    close_db()


if __name__ == "__main__":
    app.run(debug=True)

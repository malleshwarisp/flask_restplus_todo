from db import get_db
from flask_restplus import Namespace, Resource, fields

from .db_utils import *

api = Namespace("todos", description="TODO operations")

todo = api.model(
    "Todo",
    {
        "id": fields.Integer(readonly=True, description="The task unique identifier"),
        "task": fields.String(required=True, description="The task details"),
        "due_by": fields.Date(required=True, description="The tasks due date"),
        "status": fields.Integer(
            description="""The status of the task. 
                            0 -> Not Started, 
                            1 -> In Progress
                            2 -> Finished"""
        ),
    },
)


@api.route("/")
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc("list_todos")
    @api.marshal_list_with(todo)
    def get(self):
        """List all tasks"""
        results = get_all_tasks(get_db())
        output = []
        for result in results:
            output.append(
                {
                    "id": result[0],
                    "task": result[1],
                    "due_by": result[2],
                    "status": result[3],
                }
            )

        return output

    @api.doc("create_todo")
    @api.expect(todo)
    @api.marshal_with(todo, code=201)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@api.route("/<int:id>")
@api.response(404, "Todo not found")
@api.param("id", "The task identifier")
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @api.doc("get_todo")
    @api.marshal_with(todo)
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @api.doc("delete_todo")
    @api.response(204, "Todo deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        DAO.delete(id)
        return "", 204

    @api.expect(todo)
    @api.marshal_with(todo)
    def put(self, id):
        """Update a task given its identifier"""
        return DAO.update(id, api.payload)

import flask_restplus
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
        "status": fields.String(
            enum=Status._member_names_,
            description="The status of the task.",
        ),
    },
)
status = api.model(
    "Status",
    {
        "status": fields.String(
            enum=Status._member_names_,
            description="The status of the task.",
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
            output.append(task_to_dict(result))

        return output

    @api.doc("create_todo")
    @api.expect(todo)
    @api.marshal_with(todo, code=201)
    def post(self):
        """Create a new task"""
        try:
            req = api.payload
            result = create_task(
                get_db(),
                req["task"],
                date.fromisoformat(req["due_by"]),
                Status[req["status"]],
            )
            return task_to_dict(result), 201
        except ValueError:
            api.abort(422, "Invalid request parameters")


@api.route("/<int:id>")
@api.response(404, "Todo not found")
@api.param("id", "The task identifier")
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @api.doc("get_todo")
    @api.marshal_with(todo)
    def get(self, id):
        """Fetch a given resource"""
        task = get_task(get_db(), id)
        if not task:
            api.abort(404, f"Invalid task with id: {id}")
        return task_to_dict(task)

    @api.doc("delete_todo")
    @api.response(204, "Todo deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        if delete_task(get_db(), id):
            return "", 204
        api.abort(404, f"Invalid task with id: {id}")

    @api.expect(todo)
    @api.marshal_with(todo)
    def put(self, id):
        """Update a task given its identifier"""
        req = api.payload
        try:
            result = update_task(
                get_db(),
                id,
                req["task"],
                date.fromisoformat(req["due_by"]),
                Status[req["status"]],
            )
            return task_to_dict(result), 201
        except ValueError:
            api.abort(422, "Invalid Status")


@api.route("/due/<string:due_date>")
class TodoDueDate(Resource):
    @api.doc("get_todo_by_due_date")
    @api.marshal_list_with(todo)
    def get(self, due_date):
        try:
            tasks = tasks_by_due_date(get_db(), date.fromisoformat(due_date))
            return list(map(task_to_dict, tasks))
        except ValueError:
            api.abort(422, "Invalid Date")


@api.route("/overdue")
class TodoOverDue(Resource):
    @api.doc("Overdue Todos")
    @api.marshal_list_with(todo)
    def get(self):
        try:
            tasks = tasks_overdue(get_db())
            print(tasks)
            return list(map(task_to_dict, tasks))
        except ValueError:
            api.abort(422, "Invalid Date")


@api.route("/finished")
class TodoFinished(Resource):
    @api.doc("Finished Todos")
    @api.marshal_list_with(todo)
    def get(self):
        tasks = tasks_finished(get_db())
        return list(map(task_to_dict, tasks))


@api.route("/update_status/<int:id>")
class TodoStatusUpdate(Resource):
    @api.doc("Update Todo Status")
    @api.expect(status)
    def patch(self, id):
        try:
            task = update_status(get_db(), id, Status[api.payload["status"]])
            if not task:
                api.abort(404, "Invalid Task")
            return task_to_dict(task)
        except ValueError:
            api.abort(422, "Invalid Status")

import re

from flask import Blueprint, jsonify, request, render_template

from services.user_service import create_user, get_user, list_users


users = Blueprint("users", __name__)
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def error(message, status):
    return jsonify({"success": False, "error": message}), status

#For UI
@users.get("/")
def index():
    return render_template("index.html")

@users.get("/users")
def get_users():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return error("Page and limit must be positive integers", 400)

    if page < 1 or limit < 1:
        return error("Page and limit must be positive integers", 400)

    limit = min(limit, 100)
    records, total = list_users(request.args.get("search", "").strip(), page, limit)
    return jsonify({
        "success": True,
        "data": [user.to_dict() for user in records],
        "page": page,
        "limit": limit,
        "total": total,
    })


@users.post("/users")
def post_user():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return error("Request body must be a JSON object", 400)

    fields = ("name", "email", "role")
    values = {field: payload.get(field) for field in fields}
    if any(not isinstance(value, str) or not value.strip() for value in values.values()):
        return error("Name, email, and role are required", 400)

    values = {field: value.strip() for field, value in values.items()}
    if not EMAIL_PATTERN.fullmatch(values["email"]):
        return error("Email format is invalid", 400)

    try:
        user = create_user(**values)
    except ValueError as exception:
        return error(str(exception), 409)

    return jsonify({"success": True, "data": user.to_dict()}), 201


@users.get("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = get_user(user_id)
    if user is None:
        return error("User not found", 404)
    return jsonify({"success": True, "data": user.to_dict()})
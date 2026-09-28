from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from models import db
from models.user import User


def list_users(search, page, limit):
    query = User.query
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(User.name.ilike(pattern), User.email.ilike(pattern)))

    total = query.count()
    users = query.order_by(User.id).offset((page - 1) * limit).limit(limit).all()
    return users, total


def get_user(user_id):
    return db.session.get(User, user_id)


def create_user(name, email, role):
    user = User(name=name, email=email, role=role)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise ValueError("Email already exists") from error
    return user
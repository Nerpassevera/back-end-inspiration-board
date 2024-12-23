from os import environ
from flask import abort, make_response
import requests
from app.db import db


def apply_filters(cls, arguments, query):
    for attribute, value in arguments:
        if hasattr(cls, attribute):
            query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))


def validate_model(cls, cls_id):
    try:
        cls_id = int(cls_id)
    except ValueError:
        message = {"message": f"{cls.__name__} ID {cls_id} is invalid"}
        abort(make_response(message, 400))

    query = db.select(cls).where(cls.id == cls_id)
    result = db.session.scalar(query)

    if not result:
        message = {"message": f"{cls.__name__} with ID {cls_id} was not found"}
        abort(make_response(message, 404))

    return result


def create_class_instance(cls, request, required_fields, additional_data=None):
    req_body = request.get_json()

    if additional_data:
        req_body.update(additional_data)

    for field in required_fields:
        if field not in req_body:
            message = {"details": f"Invalid request: missing {field}"}
            abort(make_response(message, 400))

    try:
        new_instance = cls.from_dict(req_body)
    except KeyError as error:
        message = {"details": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(message, 400))

    db.session.add(new_instance)
    db.session.commit()

    return {cls.__name__.lower(): new_instance.to_dict()}, 201


def get_all_instances(cls, args):
    sort = args.get("sort")
    # query = db.select(cls).order_by(cls.title.desc() if sort=="desc" else cls.title)
    query = db.select(cls)

    sort_field = "message" if hasattr(cls, "message") else "title"

    if sort == "desc":
        query = query.order_by(getattr(cls, sort_field).desc())
    else:
        query = query.order_by(getattr(cls, sort_field))

    apply_filters(cls, args.items(), query)

    instances = db.session.scalars(query)
    return [instance.to_dict() for instance in instances], 200


def get_one_instance(cls, instance_id):
    instance = validate_model(cls, instance_id)

    return {cls.__name__.lower(): instance.to_dict() if instance else instance}, 200


def set_new_attributes(instance, req_body):
    for attr, value in req_body.items():
        if hasattr(instance, attr):
            setattr(instance, attr, value)


def update_instance(cls, instance_id, request, like=None):
    instance = validate_model(cls, instance_id)
    req_body = request.get_json()

    if like:
        req_body = update_likes(instance)

    set_new_attributes(instance, req_body)

    db.session.commit()
    return {cls.__name__.lower(): instance.to_dict()}, 200


def delete_instance(cls, instance_id):
    instance = validate_model(cls, instance_id)
    db.session.delete(instance)
    db.session.commit()

    return {"details": f'{cls.__name__} {instance.id} successfully deleted'}, 200


def send_card_created_message(card_message):
    request_data = {
        "channel": "#api-test-channel",  # Slack channel for tests
        # "channel": "U07GC9C8Y4X",  # My Slack account ID
        "username": "Dream Team's Inspiration Board",
        "text": f"The card \"{card_message}\" has been created!"
    }
    message_status = requests.post(
        url="https://slack.com/api/chat.postMessage",
        json=request_data,
        headers={
            "Authorization": environ.get('SLACK_API_KEY'),
            "Content-Type": "application/json"
        },
        timeout=5
    )

    return message_status.json()["ok"]


def update_likes(instance):

    instance.likes_count += 1

    return {"like_count": instance.likes_count}

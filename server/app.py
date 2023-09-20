from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages")
def messages():
    messages = Message.query.order_by(Message.created_at).all()
    messages_serialized = [m.to_dict() for m in messages]

    response = make_response(messages_serialized, 200)

    return response


@app.route("/messages", methods=["GET", "POST"])
def post_messages():
    if request.method == "GET":
        message = Message.query.first()
        message_dict = message.to_dict()
        response = make_response(message_dict, 200)
        return response

    elif request.method == "POST":
        new_post = Message(
            username=request.json.get("username"),
            body=request.json.get("body"),
            created_at=request.json.get("created_at"),
            updated_at=request.json.get("updated_at"),
        )

        db.session.add(new_post)
        db.session.commit()
        new_post_dict = new_post.to_dict()

        response = make_response(new_post_dict, 201)

        return response


@app.route("/messages/<int:id>", methods=["GET", "PATCH"])
def update_message(id):
    if request.method == "GET":
        message = Message.query.filter(Message.id == id).first()
        message_dict = message.to_dict()

        response = make_response(message_dict, 200)

        return response

    elif request.method == "PATCH":
        message = Message.query.filter(Message.id == id).first()

        new_body = request.json.get("body")

        message.body = new_body

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(message_dict, 200)

        return response


@app.route("/messages/<int:id>", methods=["GET", "DELETE"])
def delete_messages(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == "GET":
        message_dict = message.to_dict()
        response = make_response(message_dict, 200)
        return response

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response_body = {"delete successful": True, "message": "Message deleted"}

        response = make_response(response_body, 200)

        return response


if __name__ == "__main__":
    app.run(port=5555)

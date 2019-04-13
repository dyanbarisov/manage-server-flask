from models import Rack, Server
from db import Session
from flask_restful import reqparse, abort, Api, Resource
from models import Server, Rack

note_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'create_at': fields.String,
    'create_by': fields.String,
    'priority': fields.Integer
}

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('create_at')
parser.add_argument('create_by')
parser.add_argument('priority')

class ServerResource(Resource):
    #@marshal_with(note_fields)
    def get(self, id):
        note = Session.query(Server).filter(Server.id == id).first()
        if not note:
            abort(404, message="Server {} doesn't exist".format(id))
        return note

    def delete(self, id):
        note = session.query(Note).filter(Note.id == id).first()
        if not note:
            abort(404, message="Note {} doesn't exist".format(id))
        session.delete(note)
        session.commit()
        return {}, 204

    #@marshal_with(note_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        note = session.query(Note).filter(Note.id == id).first()
        note.title = parsed_args['title']
        note.description = parsed_args['description']
        note.create_at = parsed_args['create_at']
        note.create_by = parsed_args['create_by']
        note.priority = parsed_args['priority']
        session.add(note)
        session.commit()
        return note, 201


class NoteListResource(Resource):
    #@marshal_with(note_fields)
    def get(self):
        notes = session.query(Note).all()
        return notes

    #@marshal_with(note_fields)
    def post(self):
        parsed_args = parser.parse_args()
        note = Note(title=parsed_args['title'], description=parsed_args['description'],
                    create_at=parsed_args['create_at'], create_by=parsed_args['create_by'],
                    priority=parsed_args['priority'] )
        session.add(note)
        session.commit()
        return note, 201
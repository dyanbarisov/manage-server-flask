from flask_restful import reqparse, abort, Resource, fields, marshal_with
from models import Server, Rack
from datetime import datetime
from dateutil.relativedelta import relativedelta
from threading import Thread
import random
from time import sleep
from db import Session
from sqlalchemy import desc

rack_fields = {
    'id': fields.Integer,
    'create_date': fields.DateTime,
    'change_date': fields.DateTime,
    'capacity': fields.String,
    'server_count': fields.Integer
}

server_fields = {
    'id': fields.Integer,
    'create_date': fields.DateTime,
    'change_date': fields.DateTime,
    'expired_date': fields.DateTime,
    'state': fields.String,
    'rack': fields.Integer
}

parser = reqparse.RequestParser()
parser.add_argument('capacity')
parser.add_argument('state')
parser.add_argument('rack')
parser.add_argument('sort_by')
parser.add_argument('months')
parser.add_argument('months')


class RackResource(Resource):
    @marshal_with(rack_fields)
    def get(self, id):
        rack = Session.query(Rack).filter(Rack.id == id).first()
        if not rack:
            abort(404, message="Rack {} doesn't exist".format(id))
        return rack

    def delete(self, id):
        rack = Session.query(Rack).filter(Rack.id == id).first()
        if not rack:
            abort(404, message="Rack {} doesn't exist".format(id))
        Session.delete(rack)
        Session.commit()
        return {}, 204

    @marshal_with(rack_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        rack = Session.query(Rack).filter(Rack.id == id).first()
        rack.title = parsed_args['create_date']
        rack.description = parsed_args['change_date']
        rack.create_at = parsed_args['capacity']
        Session.add(rack)
        Session.commit()
        return rack, 201


class RackListResource(Resource):
    @marshal_with(rack_fields)
    def get(self):
        parsed_args = parser.parse_args()
        sort_by = 'change_date' if parsed_args['sort_by'] == 'change_date' else 'id'
        racks = Session.query(Rack).order_by(desc(sort_by)).all()
        return racks

    @marshal_with(rack_fields)
    def post(self):
        parsed_args = parser.parse_args()
        rack = Rack(
            create_date=datetime.now(),
            change_date=datetime.now(),
            capacity=parsed_args['capacity']
        )
        Session.add(rack)
        Session.commit()
        return rack, 201


class ServerResource(Resource):
    def activate_server(self, server_id, months):
        sleep(random.randint(3, 20))
        server = Session.query(Server).filter(Server.id == server_id).first()
        if server.state == Server.SERVER_STATES['Deleted']:
            return
        months = Server.DEFAULT_MONTHS_PAID if months is None else int(months)
        server.state = Server.SERVER_STATES['Active']
        dt_now = datetime.now()
        server.expired_date = dt_now + relativedelta(minute=months)
        server.change_date = dt_now
        Session.add(server)
        Session.commit()

    def change_state(self, server_id, server_state, months):
        server = Session.query(Server).filter(Server.id == server_id).first()
        if server_state == Server.SERVER_STATES['Paid'] and server.state == Server.SERVER_STATES['Unpaid'] or \
                server_state == Server.SERVER_STATES['Deleted']:
            server.state = server_state
            server.change_date = datetime.now()
            Session.add(server)
            Session.commit()
            if server_state == Server.SERVER_STATES['Paid']:
                Thread(target=self.activate_server, args=(server_id, months,)).start()
            return server, 201
        abort(406, message="The server transition to the paid state is not available.")

    @marshal_with(server_fields)
    def get(self, id):
        server = Session.query(Server).filter(Server.id == id).first()
        if not server:
            abort(404, message="Server {} doesn't exist".format(id))
        return server

    def delete(self, id):
        server = Session.query(Server).filter(Server.id == id).first()
        if not server:
            abort(404, message="Server {} doesn't exist".format(id))
        Session.delete(server)
        Session.commit()
        return {}, 204

    @marshal_with(server_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        server = Session.query(Server).filter(Server.id == id).first()
        server.title = parsed_args['create_date']
        server.change_date = parsed_args['change_date']
        server.create_at = parsed_args['capacity']
        Session.add(server)
        Session.commit()
        return server, 201

    @marshal_with(server_fields)
    def patch(self, id):
        parsed_args = parser.parse_args()
        state = parsed_args['state']
        month = parsed_args['months']
        if state:
            self.change_state(id, state, month)


class ServerListResource(Resource):
    @marshal_with(server_fields)
    def get(self):
        parsed_args = parser.parse_args()
        sort_by = 'change_date' if parsed_args['sort_by'] == 'change_date' else 'id'
        servers = Session.query(Rack).order_by(desc(sort_by)).all()
        return servers

    @marshal_with(server_fields)
    def post(self):
        parsed_args = parser.parse_args()
        rack_id = parsed_args['rack']
        rack = Session.query(Rack).filter(Rack.id == rack_id).first()
        if not rack:
            abort(404, message="Rack {} doesn't exist".format(rack_id))
        if not rack.check_free_slot():
            abort(404, message="Rack {} is full".format(rack_id))
        server = Server(
            create_date=datetime.now(),
            change_date=datetime.now(),
            rack=rack_id
        )
        rack.server_count += 1
        rack.change_date = datetime.now()
        Session.add(server)
        Session.add(rack)
        Session.commit()
        return server, 201

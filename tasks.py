from models import Server
from db import Session
from datetime import datetime


def check_expired_servers():
    dt_now = datetime.now()
    servers = Session.query(Server).filter(Server.state == Server.ACTIVE, Server.expired_date < dt_now)
    for server in servers:
        server.state = Server.UNPAID
        Session.add(server)
    Session.commit()

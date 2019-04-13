from models import Server
from db import Session
from datetime import datetime


def check_expired_servers():
    dt_now = datetime.now()
    print(str(dt_now))
    servers = Session.query(Server).filter(Server.state == Server.SERVER_STATES['Active'], Server.expired_date < dt_now)
    print(servers.count())
    for server in servers:
        server.state = Server.SERVER_STATES['Unpaid']
        Session.add(server)
    Session.commit()


from models import Server
from db import Session
from datetime import datetime
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
log.addHandler(console)


def check_expired_servers():
    dt_now = datetime.now()
    servers = Session.query(Server).filter(Server.state == Server.ACTIVE, Server.expired_date < dt_now)
    for server in servers:
        server.state = Server.UNPAID
        Session.add(server)
        log.info('Server {} deactivated'.format(server.id))
    Session.commit()

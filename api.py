from flask import Flask
from flask_restful import Api
from resources import *
from db import init_db
import atexit
from apscheduler.scheduler import Scheduler
from tasks import check_expired_servers

app = Flask(__name__)
api = Api(app)

cron = Scheduler()
cron.add_interval_job(check_expired_servers, seconds=30)
cron.start()
atexit.register(lambda: cron.shutdown(wait=False))


@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()


api.add_resource(RackResource, '/racks/<string:id>', endpoint='racks')
api.add_resource(RackListResource, '/racks/', endpoint='rack')
api.add_resource(ServerResource, '/servers/<string:id>', endpoint='servers')
api.add_resource(ServerListResource, '/servers/', endpoint='server')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

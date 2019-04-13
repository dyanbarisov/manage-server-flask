from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///./main.db', connect_args={'check_same_thread': False})
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))


def init_db():
    import models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

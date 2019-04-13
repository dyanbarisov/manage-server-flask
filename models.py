from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy_utils.types.choice import ChoiceType


class Rack(Base):
    CAPACITY_TYPES = [
        ('small', 10),
        ('big', 20)
    ]

    __tablename__ = 'racks'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    change_date = Column(DateTime)
    capacity = Column(ChoiceType(CAPACITY_TYPES))
    servers = relationship('Server', lazy='dynamic')
    server_count = Column(Integer, default=0)

    def check_free_slot(self):
        if self.server_count < self.capacity.value:
            return True

    def __repr__(self):
        return '<Rack {}>'.format(self.id)


class Server(Base):
    UNPAID = '0'
    PAID = '1'
    ACTIVE = '2'
    DELETED = '3'
    SERVER_STATES = {
        'Unpaid': UNPAID,
        'Paid': PAID,
        'Active': ACTIVE,
        'Deleted': DELETED
    }
    STATE_MATRIX = {
        DELETED: lambda st: False,
        UNPAID: lambda st: st == Server.PAID,
        PAID: lambda st: st == Server.DELETED,
        ACTIVE: lambda st: st == Server.DELETED
    }

    DEFAULT_MONTHS_PAID = 1

    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    change_date = Column(DateTime)
    expired_date = Column(DateTime)
    state = Column(String, nullable=False, default=0)
    rack = Column(Integer, ForeignKey('racks.id'))

    def __repr__(self):
        return '<Server {}>'.format(self.id)

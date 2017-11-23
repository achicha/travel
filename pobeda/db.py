import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# db_connector
class DataAccessLayer:
    """ access to DB fabric"""

    def __init__(self, conn_string, base, echo=False):
        self.engine = None
        self.session = None
        self.conn = None
        self.conn_string = conn_string
        self.echo = echo
        self.Base = base

    def connect(self):
        self.engine = create_engine(self.conn_string, echo=self.echo)
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

# models
from datetime import datetime as dt
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.exc import IntegrityError

TicketsBase = declarative_base()


class Ticket(TicketsBase):
    __tablename__ = 'ticket'
    __table_args__ = (UniqueConstraint('flight_from', 'flight_to', 'date', name='unique_flight'),)

    id = Column(Integer(), primary_key=True)
    flight_from = Column(String(255), nullable=False)
    flight_to = Column(String(255), nullable=False)
    date = Column(String(255), nullable=False, default=dt.now().strftime('%d-%m-%Y'))
    cost = Column(String(), nullable=False)
    update_time = Column(DateTime, nullable=False,  default=dt.now, onupdate=dt.now)
    sent_to_telegram = Column(DateTime)

    def __repr__(self):
        return "From='{self.flight_from}', " \
                "To='{self.flight_to}', " \
                "Date='{self.date}'"\
                "cost='{self.cost}'"\
                "sent_to_telegram='{self.sent_to_telegram}'".format(self=self)


# initial_create
def init_db(session):

    # test dataset
    tickets = [
        ('Москва (Внуково)', 'Екатеринбург', dt.strptime('11-05-2017', '%d-%m-%Y')),
        ('Москва (Внуково)', 'Владивосток', dt.strptime('07-07-2017', '%d-%m-%Y')),
        ('Москва (Внуково)', 'Сочи', dt.strptime('04-02-2016', '%d-%m-%Y')),
        ('Милан', 'Москва (Внуково)', dt.strptime('13-05-2017', '%d-%m-%Y'))
    ]

    # try to insert data, maybe they are already exist
    try:
        session.bulk_insert_mappings(Ticket,
                                     [
                                         # create comprehension
                                         dict(
                                             flight_from=flight_from,
                                             flight_to=flight_to,
                                             date=date
                                         )
                                         for flight_from, flight_to, date in tickets
                                     ])
        session.commit()

    except IntegrityError:
        print('IntegrityError error: {}'.format(traceback.format_exc()))
        session.rollback()

import traceback
from datetime import datetime as dt

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.exc import IntegrityError

TicketsBase = declarative_base()


class PobedaTickets(TicketsBase):
    __tablename__ = 'pobeda_tickets'
    __table_args__ = (UniqueConstraint('airport_from', 'airport_to', 'date', name='unique_flight'),)

    id = Column(Integer(), primary_key=True)
    airport_from = Column(String(255), ForeignKey('pobeda_airports.city_name_ru'), nullable=False)
    airport_to = Column(String(255), ForeignKey('pobeda_airports.city_name_ru'), nullable=False)
    date = Column(DateTime(), nullable=False)
    cost = Column(Integer(), nullable=False)
    update_time = Column(DateTime(), nullable=False, default=dt.now, onupdate=dt.now)
    sent_to_telegram = Column(DateTime())

    def __repr__(self):
        return "{} | {} -> {} ={}".format(dt.strftime(self.date, '%d-%m-%Y'),
                                          self.airport_from,
                                          self.airport_to,
                                          self.cost
                                          )
        # "sent_to_telegram='{self.sent_to_telegram}'"


class PobedaDestination(TicketsBase):
    __tablename__ = 'pobeda_destination'
    __table_args__ = (UniqueConstraint('airport_code_from', 'airport_code_to', name='unique_destination'),)

    # todo: route add time, and last update tickets time
    id = Column(Integer(), primary_key=True)
    airport_code_from = Column(String(255), ForeignKey('pobeda_airports.short_code'), nullable=False)
    airport_code_to = Column(String(255), ForeignKey('pobeda_airports.short_code'), nullable=False)
    update_time = Column(DateTime, nullable=False, default=dt.now, onupdate=dt.now)


class PobedaAirports(TicketsBase):
    __tablename__ = 'pobeda_airports'
    __table_args__ = (UniqueConstraint('short_code', 'city_name_en', name='unique_airports'),)

    id = Column(Integer(), primary_key=True)
    short_code = Column(String(255), nullable=False)
    city_name_en = Column(String(255), nullable=False)
    city_name_ru = Column(String(255), nullable=False)
    update_time = Column(DateTime, nullable=False, default=dt.now, onupdate=dt.now)


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
        session.bulk_insert_mappings(PobedaTickets,
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

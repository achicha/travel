import traceback
from datetime import datetime as dt

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

CBase = declarative_base()


class Tickets(CBase):
    __tablename__ = 'tickets'
    __table_args__ = (UniqueConstraint('origin_airport', 'destination_airport', 'date', 'price', 'number_of_changes',
                                       name='unique_flight'),)

    id = Column(Integer(), primary_key=True)
    origin_airport = Column(String(255), nullable=False)
    destination_airport = Column(String(255), nullable=False)
    date = Column(DateTime(), nullable=False)
    price = Column(Integer(), nullable=False)
    number_of_changes = Column(Integer(), default=0)
    gate = Column(String(255))  # who selling the ticket

    update_time = Column(DateTime(), nullable=False, default=dt.now, onupdate=dt.now)
    sent_to_telegram = Column(DateTime())

    def __str__(self):
        return "{}| from {} -> to {} ={}rub".format(dt.strftime(self.date, '%d-%m-%Y'),
                                                    self.origin_airport,
                                                    self.destination_airport,
                                                    self.price
                                                    )

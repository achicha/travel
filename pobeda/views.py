from _datetime import datetime as dt, timedelta as td
from collections import namedtuple
from .db import DataAccessLayer, Ticket, init_db, TicketsBase
from sqlalchemy.exc import IntegrityError, InvalidRequestError


class TicketsParser:
    def __init__(self, conn_string, base=TicketsBase, echo=False):
        self.dal = DataAccessLayer(conn_string, base, echo=echo)

    def setup(self):
        self.dal.connect()
        self.dal.session = self.dal.Session()

    def teardown(self):
        self.dal.session.close()

    def create_db(self):
        """
            init db first time
        :return:
        """
        init_db(self.dal.session)

    def get_new_tickets(self):
        """
            Return newly added tickets from Database.
        :return: newly added ticket from DB.
        """
        return self.dal.session.query(Ticket).filter_by(sent_to_telegram=None).all()

    def after_sent_to_telegram(self, ticket):
        ticket_obj = Ticket()
        ticket_obj.flight_from = ticket.flight_from
        ticket_obj.flight_to = ticket.flight_to
        ticket_obj.date = ticket.date
        ticket_obj.cost = ticket.cost
        new_ticket = self.dal.session.query(Ticket).filter_by(flight_from=ticket_obj.flight_from,
                                                              flight_to=ticket_obj.flight_to,
                                                              date=ticket_obj.date,
                                                              cost=ticket_obj.cost).first()
        new_ticket.sent_to_telegram = dt.now()
        self.dal.session.commit()

    def add_tickets(self, tickets):
        """
            Add new ticket to Database
        :param ticket: [(flight_from:str,flight_to:str,date:datetime),]:list
        :return:
        """
        # Structure = namedtuple('Tick', ['flight_from', 'flight_to', 'date', 'cost'])
        # _ticket = Structure(flight_from='Москва (Внуково)', flight_to='Владикавказ', date='15 янв 2018', cost='1 499руб')

        for ticket in tickets:
            ticket_obj = Ticket()
            ticket_obj.flight_from = ticket.flight_from
            ticket_obj.flight_to = ticket.flight_to
            ticket_obj.date = ticket.date
            ticket_obj.cost = ticket.cost
            if self.dal.session.query(Ticket).filter_by(flight_from=ticket_obj.flight_from,
                                                        flight_to=ticket_obj.flight_to,
                                                        date=ticket_obj.date).count() < 1:
                try:
                    self.dal.session.add(ticket_obj)
                except IntegrityError:
                    continue
                except InvalidRequestError:  # UNIQUE constraint failed
                    continue
                else:
                    self.dal.session.commit()
        return True

    def remove_old_tickets(self, days=30):
        """
            Remove update_time for old tickets (maybe they will be available again)
        :param days: number of days
        :return: True/False
        """
        results = self.dal.session.query(Ticket).filter(Ticket.sent_to_telegram < dt.now() - td(days))
        results.delete()
        self.dal.session.commit()

        return True

from datetime import datetime as dt, timedelta as td
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from helpers.db import DataAccessLayer
from .models import PobedaTickets, init_db, TicketsBase, PobedaAirports, PobedaDestination


class PobedaTicketsParser:
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
        # todo price filter
        return self.dal.session.query(PobedaTickets).filter_by(sent_to_telegram=None).all()

    def after_sent_to_telegram(self, tickets):
        for ticket in tickets:
            ticket_obj = PobedaTickets()
            ticket_obj.airport_from = ticket.airport_from
            ticket_obj.airport_to = ticket.airport_to
            ticket_obj.date = ticket.date
            ticket_obj.cost = ticket.cost
            new_ticket = self.dal.session.query(PobedaTickets).filter_by(airport_from=ticket_obj.airport_from,
                                                                         airport_to=ticket_obj.airport_to,
                                                                         date=ticket_obj.date,
                                                                         cost=ticket_obj.cost).first()
            new_ticket.sent_to_telegram = dt.now()
        self.dal.session.commit()

    def add_tickets(self, tickets):
        """
            Add new ticket to Database
        :param tickets: [(airport_from:str,airport_to:str,date:datetime),]:list
        :return:
        """
        # Structure = namedtuple('Tick', ['airport_from', 'airport_to', 'date', 'cost'])
        # _ticket = Structure(airport_from='Москва (Внуково)', airport_to='Владикавказ', date='15 янв 2018', cost='1 499руб')

        for ticket in tickets:
            ticket_obj = PobedaTickets()
            ticket_obj.airport_from = ticket.airport_from
            ticket_obj.airport_to = ticket.airport_to
            ticket_obj.date = ticket.date
            ticket_obj.cost = ticket.cost

            if self.dal.session.query(PobedaTickets).filter_by(airport_from=ticket_obj.airport_from,
                                                               airport_to=ticket_obj.airport_to,
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
        results = self.dal.session.query(PobedaTickets).filter(PobedaTickets.sent_to_telegram < dt.now() - td(days))
        results.delete()
        self.dal.session.commit()

        return True

    def add_new_airport(self, airports: list()):
        """
            find all airports where Pobeda is flight to
        :param: airports: [(code, city_en, city_ru),]
        :return:
        """
        for airport in airports:
            airport_obj = PobedaAirports()
            airport_obj.short_code = airport[0]
            airport_obj.city_name_en = airport[1]
            airport_obj.city_name_ru = airport[2]

            if self.dal.session.query(PobedaAirports) \
                    .filter_by(city_name_en=airport_obj.city_name_en,
                               short_code=airport_obj.short_code).count() < 1:
                try:
                    self.dal.session.add(airport_obj)
                except IntegrityError:
                    continue
                except InvalidRequestError:  # UNIQUE constraint failed
                    continue
                else:
                    self.dal.session.commit()
        return True

    def get_all_destinations(self, hometown):
        """
            Return all destinations from hometown.
        :return:
        """
        return self.dal.session.query(PobedaDestination.airport_code_to).filter_by(airport_code_from=hometown).all()

    def add_new_destination(self, home_town, destinations: list()):
        """
            add all relationships between home town and destination city
        :param home_town: departure city
        :param destinations: city's list
        :return:
        """
        for destination in destinations:
            city_obj = PobedaDestination()
            city_obj.airport_code_from = home_town
            city_obj.airport_code_to = destination

            if self.dal.session.query(PobedaDestination) \
                    .filter_by(airport_code_from=city_obj.airport_code_from,
                               airport_code_to=city_obj.airport_code_to).count() < 1:
                try:
                    self.dal.session.add(city_obj)
                except IntegrityError:
                    continue
                except InvalidRequestError:  # UNIQUE constraint failed
                    continue
                else:
                    self.dal.session.commit()
        return True

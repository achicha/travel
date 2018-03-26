from datetime import datetime as dt, timedelta as td
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import and_, desc

from database.db_connector import DataAccessLayer
from database.models import CBase, Tickets, Airports


class DBConnector:
    def __init__(self, conn_string, base=CBase, echo=False):
        self.dal = DataAccessLayer(conn_string, base, echo=echo)

    def setup(self):
        self.dal.connect()
        self.dal.session = self.dal.Session()

    def teardown(self):
        self.dal.session.close()

    def get_new_tickets(self, min_price):
        """
            Return newly added tickets from Database.
        :return: newly added ticket from DB.
        """
        return self.dal.session.query(Tickets) \
            .filter(and_(Tickets.sent_to_telegram == None, Tickets.price < min_price)).order_by(Tickets.price).all()

    def update_telegram_status(self, tickets):
        """
        After message was sent to Telegram, need to update sent_to_telegram field in DB
        :param tickets:
        :return:
        """
        for ticket in tickets:
            new_ticket = self.dal.session.query(Tickets) \
                .filter_by(origin_airport=ticket.origin_airport,
                           destination_airport=ticket.destination_airport,
                           date=ticket.date,
                           price=ticket.price,
                           number_of_changes=ticket.number_of_changes,
                           resource=ticket.resource).first()
            if new_ticket:
                new_ticket.sent_to_telegram = dt.now()
                self.dal.session.commit()
            else:
                print('wrong ticket')

    def add_tickets(self, tickets):
        """
            Add new ticket to Database
        :param tickets: [(airport_from:str,airport_to:str,date:datetime),]:list
        :return:
        """
        # {'value': 5140.0, 'return_date': None, 'number_of_changes': 0, 'gate': 'Pobeda', 'depart_date': '2018-04-23'}

        for ticket in tickets:
            ticket_obj = Tickets(origin_airport=ticket['origin_airport'],
                                 destination_airport=ticket['destination_airport'],
                                 date=dt.strptime(ticket['depart_date'], '%Y-%m-%d'),
                                 price=ticket['value'],
                                 number_of_changes=ticket['number_of_changes'],
                                 gate=ticket['gate'],
                                 resource=ticket['resource'])

            if self.dal.session.query(Tickets) \
                .filter_by(origin_airport=ticket_obj.origin_airport,
                           destination_airport=ticket_obj.destination_airport,
                           date=ticket_obj.date,
                           price=ticket_obj.price,
                           number_of_changes=ticket_obj.number_of_changes,
                           resource=ticket_obj.resource).count() < 1:
                try:
                    self.dal.session.add(ticket_obj)
                except IntegrityError:
                    continue
                except InvalidRequestError:  # UNIQUE constraint failed
                    continue
                else:
                    self.dal.session.commit()
            else:
                print('ticket already exists')
        return True

    def remove_old_tickets(self, days=15):
        """
            Remove update_time for old tickets (maybe they will be available again)
        :param days: number of days
        :return: True/False
        """
        try:
            results = self.dal.session.query(Tickets).filter(Tickets.update_time < dt.now() - td(days))
            results.delete()
            self.dal.session.commit()

            return True
        except Exception:
            return False

    def add_new_airport(self, new_airports):
        """
         Add new airport code <-> city name map to DB
        :param new_airports: dictionary like {'airport_code': 'city_name'}
        :return:
        """

        for airport in new_airports:
            airport_obj = Airports()
            airport_obj.short_code = airport
            airport_obj.city_name = new_airports[airport]

            if self.dal.session.query(Airports) \
                    .filter_by(city_name=airport_obj.city_name,
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

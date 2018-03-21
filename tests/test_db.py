import traceback
from datetime import datetime as dt, timedelta as td
from sqlalchemy.exc import IntegrityError
from database.views import DBConnector
from database.models import Tickets, CBase


class TestDatabase:
    def setup_class(self):
        """class setup"""

        self.db = DBConnector('sqlite:///:memory:', CBase, echo=False)
        self.db.setup()
        self.insert_data(self.db.dal.session)

    @classmethod
    def insert_data(cls, session):
        # test dataset
        tickets = [
            ('MOW', 'LWN', dt.strptime('11-05-2017', '%d-%m-%Y'), 1000),
            ('LWN', 'MOW', dt.strptime('07-07-2017', '%d-%m-%Y'), 1200),
            ('EVN', 'SVX', dt.strptime('04-02-2016', '%d-%m-%Y'), 1500),
            ('SVX', 'EVN', dt.strptime('13-05-2017', '%d-%m-%Y'), 2000)
        ]

        # try to insert data, maybe they are already exist
        try:
            session.bulk_insert_mappings(Tickets,
                                         [
                                             # create comprehension
                                             dict(
                                                 origin_airport=flight_from,
                                                 destination_airport=flight_to,
                                                 date=date,
                                                 price=price
                                             )
                                             for flight_from, flight_to, date, price in tickets
                                         ])
            session.commit()

        except IntegrityError:
            print('IntegrityError error: {}'.format(traceback.format_exc()))
            session.rollback()

    def test_get_new_tickets(self):
        # get new ticket
        tickets = self.db.get_new_tickets(5000)
        assert tickets[0].sent_to_telegram is None
        assert tickets[0].origin_airport.strip() == 'MOW'

        # update telegram status
        self.db.set_telegram_status_after_update(tickets)
        assert isinstance(tickets[0].sent_to_telegram, dt)

    def test_add_tickets(self):
        tickets = [{'origin_airport': 'MOW', 'destination_airport': 'LWN',
                    'value': 5500.0, 'return_date': None, 'number_of_changes': 0,
                    'gate': 'Pobeda', 'depart_date': '2018-04-23'},
                   {'origin_airport': 'MOW', 'destination_airport': 'LWN',
                    'value': 5500.0, 'return_date': None, 'number_of_changes': 0,
                    'gate': 'Pobeda', 'depart_date': '2018-04-23'}
                   ]
        self.db.add_tickets(tickets)

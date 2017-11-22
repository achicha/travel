import datetime
from collections import namedtuple
from .db import DataAccessLayer, Ticket, init_db, TicketsBase
from sqlalchemy.exc import IntegrityError


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

    def get_last_n_tickets(self, n):
        """
            Return N last tickets from Database.
        :param n: number of ticket
        :return: N last ticket
        """
        res = {}
        return

    def add_new_ticket(self, ticket):
        """
            Add new ticket to Database
        :param ticket: (flight_from:str,flight_to:str,date:datetime)
        :return:
        """
        #_t = namedtuple('Tick', ['flight_from', 'flight_to', 'date', 'cost'])
        #_ticket = _t('Moscow', 'Paris', datetime.datetime.now().strftime('%d-%m-%Y'))
        # todo fix this method
        ticket_obj = Ticket()
        ticket_obj.flight_from = ticket.flight_from
        ticket_obj.flight_to = ticket.flight_to
        ticket_obj.date = ticket.date
        ticket_obj.cost = ticket.cost

        try:
            # print(ticket_obj)
            self.dal.session.merge(ticket_obj)
            self.dal.session.commit()
        except IntegrityError:
            pass
        return True

    def remove_old_tickets(self, days=15):
        """
            Remove update_time for old tickets (maybe they will be available again)
        :param days: number of days
        :return: True/False
        """
        return


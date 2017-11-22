from .db import DataAccessLayer, Ticket, init_db, TicketsBase


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
        :param ticket:
        :return:
        """
        return

    def remove_old_tickets(self, days=15):
        """
            Remove update_time for old tickets (maybe they will be available again)
        :param days: number of days
        :return: True/False
        """
        return


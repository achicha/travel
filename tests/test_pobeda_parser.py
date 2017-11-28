from collections import namedtuple

from pobeda.pobeda_parser import fetch, Structure
from pobeda.views import TicketsParser
import pytest


class TestPobeda:

    def test_fetch(self):
        # init db
        tickets_db = TicketsParser('sqlite:///:memory:', echo=False)
        tickets_db.setup()

        # fetch
        one_way = fetch(min_price=2000, max_price=2000)
        assert len(one_way) > 0
        assert isinstance(one_way[0], Structure)
        two_ways = fetch(min_price=2000, max_price=2000, return_flight=True)
        assert len(two_ways) > 0

        # add tickets to DB
        tickets_db.add_tickets(two_ways)
        assert len(tickets_db.get_new_tickets()) > 0





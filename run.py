#!/usr/bin/env python3.5

import json
from collections import namedtuple
from datetime import datetime as dt, timedelta as td
import click
from pobeda.views import TicketsParser
from pobeda.pobeda_parser import fetch


@click.command()
# @click.argument('days')
@click.option('--debug', '-d', type=bool, is_flag=True, help='debug mode on, for testing purpose only ')
@click.option('--init', '-i', type=bool, is_flag=True, help='init config, write data from config to DB ')
def cli(debug, init):
    if debug:
        lvl = 'DEBUG'
        echo = True
        print('debug')
    else:
        lvl = False
        echo = False

    click.echo('downloading')
    # init parsers/db
    # todo change sqlite to mysql/postrgesql
    tickets_db = TicketsParser('sqlite:///pobeda_tickets', echo=echo)  # ('sqlite:///:memory:')
    tickets_db.setup()

    # insert init data
    if init:
        tickets_db.create_db()

    # download data
    found_tickets = fetch(min_price=1500, max_price=1500,
                          aeroport_from='VKO', aeroport_to='', return_flight=True)

    tickets_db.add_tickets(found_tickets)

    # sent to telegram
    new_tickets = tickets_db.get_new_tickets()
    for t in new_tickets:
        #print(t) # todo sent msg to telegram bot here
        tickets_db.after_sent_to_telegram(t)

    tickets_db.remove_old_tickets()

    # exit
    tickets_db.teardown()
    click.echo('script finished')


if __name__ == "__main__":
    cli(obj={})

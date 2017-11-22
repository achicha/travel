#!/usr/bin/env python3.5

import json
from collections import namedtuple
from datetime import datetime as dt, timedelta as td
import click
from pobeda.views import TicketsParser

@click.command()
#@click.argument('days')
@click.option('--debug', '-d', type=bool, is_flag=True, help='debug mode on, for testing purpose only ')
@click.option('--init', '-i', type=bool, is_flag=True, help='init config, write data from config to DB ')
def cli(debug, init):

    if debug:
        lvl = 'DEBUG'
        print('debug')
    else:
        lvl = False

    click.echo('downloading')
    # init parsers/db
    # todo change sqlite to mysql/postrgesql
    tickets_db = TicketsParser('sqlite:///pobeda_tickets')  #('sqlite:///:memory:')
    tickets_db.setup()

    # insert init date
    if init:
        tickets_db.create_db()


    # # parse holidays from investing
    # investing_holidays = p.holidays_from_investing(input_date, configured_countries)
    #
    # if not investing_holidays:
    #     tickets_db.teardown()
    #     exit(0)
    #

    tickets_db.teardown()
    click.echo('script finished')

if __name__ == "__main__":
    cli(obj={})

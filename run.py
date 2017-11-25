#!/usr/bin/env python3.5
import asyncio

import click

from pobeda.views import TicketsParser
from pobeda.pobeda_parser import fetch
from telegram_bot import tele_bot
from settings import DB


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
    tickets_db = TicketsParser(DB, echo=echo)  # ('sqlite:///:memory:')
    tickets_db.setup()

    # insert init data
    if init:
        tickets_db.create_db()

    # download data
    found_tickets = fetch(min_price=1000, max_price=1000,
                          aeroport_from='VKO', aeroport_to='', return_flight=True)

    tickets_db.add_tickets(found_tickets)

    # sent to telegram
    new_tickets = tickets_db.get_new_tickets()
    if new_tickets:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(tele_bot.handler(loop, new_tickets))
        except Exception as e:
            print('Error create server: %r' % e)
        else:
            tickets_db.after_sent_to_telegram(new_tickets)
        finally:
            loop.close()

    # exit
    tickets_db.remove_old_tickets()
    tickets_db.teardown()
    click.echo('script finished')


if __name__ == "__main__":
    cli(obj={})

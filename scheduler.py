import asyncio

import click

from pobeda.views import TicketsParser
from pobeda.pobeda_parser import fetch
from telegram_bot import tele_bot

import schedule
import time


def cli(debug=False, init=False):
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
    print(time.time())

schedule.every(10).seconds.do(cli)

while True:
    schedule.run_pending()
    time.sleep(5)
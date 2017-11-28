#!/usr/bin/env python3.5
import traceback
from datetime import datetime as dt

import click

from helpers.msg_sender import send
from pobeda.pobeda_parser import fetch
from pobeda.views import TicketsParser
from settings import DATABASE_URL, HEROKU_URL, URL_SUFFIX


@click.command()
# @click.argument('days')
@click.option('--debug', '-d', type=bool, is_flag=True, help='debug mode on, for testing purpose only ')
@click.option('--init', '-i', type=bool, is_flag=True, help='init config, write data from config to DB ')
def cli(debug, init):
    click.echo('start')
    if debug:
        lvl = 'DEBUG'
        echo = True
        print('debug')
    else:
        lvl = 'INFO'
        echo = False

    # init logger
    try:
        from helpers.log import LogMixin
        Log = LogMixin(parser_name='pobeda', level=lvl)
        logger = Log.logger
    except BaseException:
        import logging
        logger = logging.getLogger()

    # init parsers/db
    tickets_db = TicketsParser(DATABASE_URL, echo=echo)  # ('sqlite:///:memory:')
    tickets_db.setup()
    logger.debug('ticket_db set up successful')

    # insert init data
    if init:
        tickets_db.create_db()

    # download data
    found_tickets = fetch(min_price=1000, max_price=1000,
                          aeroport_from='VKO', aeroport_to='', return_flight=True)
    tickets_db.add_tickets(found_tickets)
    logger.info('total found_tickets: {}'.format(len(found_tickets)))

    # sent to telegram
    new_tickets = tickets_db.get_new_tickets()
    logger.info('total new_tickets found: {}'.format(len(new_tickets)))
    if new_tickets:
        try:
            if debug:
                [print(ticket) for ticket in new_tickets]
            else:
                send(HEROKU_URL + URL_SUFFIX, '\n'.join([str(ticket) for ticket in new_tickets]))
        except Exception:
            logger.error('Send to telegram error: \n {}'.format(traceback.format_exc()))
        else:
            tickets_db.after_sent_to_telegram(new_tickets)

    # exit
    tickets_db.remove_old_tickets()
    tickets_db.teardown()
    click.echo('script finished')
    logger.info('script is finished at {} UTC'.format(
        dt.strftime(dt.utcfromtimestamp(int(dt.now().timestamp())), '%Y-%m-%d %H:%M:%S')
    ))


if __name__ == "__main__":

    cli(obj={})

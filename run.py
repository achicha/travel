#!/usr/bin/env python3.5
import traceback
from datetime import datetime as dt

import click

from helpers.msg_sender import send
from pobeda.pobeda_parser import fetch, airports, destinations, run_webdriver
from pobeda.views import PobedaTicketsParser
from settings import DATABASE_URL, HEROKU_URL, URL_SUFFIX, WEBDRIVER_PATH


@click.command()
@click.argument('city_from')
@click.option('--city_to', '-c', type=str, help='destination town, if None than search for all cities')
@click.option('--price', '-p', type=int, default=1000, help='maximum ticket price')
@click.option('--debug', '-d', type=bool, is_flag=True, help='debug mode on, for testing purpose only ')
@click.option('--init', '-i', type=bool, is_flag=True, help='add airports and flights to DB ')
def cli(city_from, city_to, price,  debug, init):
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
    tickets_db = PobedaTicketsParser(DATABASE_URL, echo=False)  # ('sqlite:///:memory:')
    tickets_db.setup()
    logger.debug('ticket_db set up successful')

    # insert init data
    if init:
        # insert new found airports
        found_airports = airports()
        tickets_db.add_new_airport(found_airports)
        logger.info('total found_airports: {}'.format(len(found_airports)))
        # insert new found destinations
        found_destinations = destinations(city_from)
        tickets_db.add_new_destination(city_from, found_destinations)
        logger.info('total found_destinations: {}'.format(len(found_destinations)))
        exit(0)

    # download data
    # todo: add separate method for discounts page
    # found_tickets = fetch(min_price=1000, max_price=1000,
    #                       aeroport_from=city_from, aeroport_to='', return_flight=True)
    # tickets_db.add_tickets(found_tickets)
    # logger.info('total found_tickets: {}'.format(len(found_tickets)))

    # todo: city_to if we do not need all tickets. city_to should be a list [city1, city2..]
    # find all destination from hometown
    routes = tickets_db.get_all_destinations(city_from)

    # download all tickets
    hometown_city = tickets_db.get_city_name(city_from)[0]
    for route in routes:
        route_tickets = run_webdriver(WEBDRIVER_PATH, hometown_city, route[0])
        if route_tickets:
            tickets_db.add_tickets(route_tickets)  # add found tickets to DB
            logger.info('tickets={}, city_to={}'.format(len(route_tickets), route))

    # new low price tickets
    new_tickets = tickets_db.get_new_tickets(price)
    logger.info('total new_tickets found: {}'.format(len(new_tickets)))

    # sent new tickets to telegram
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

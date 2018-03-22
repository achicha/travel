import traceback
from datetime import datetime as dt, timedelta as td
import click
from parsers.aviasales import AviaSalesParser
from parsers.msg_sender import send
from database.views import DBConnector
from settings import DATABASE_URL, HEROKU_URL, URL_SUFFIX, CHAT_ID


# set default help options
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', '-d', type=bool, is_flag=True,
              help='debug mode on, for testing purpose only ')
@click.pass_context
def cli(ctx, debug):
    """Travel parsers. examples: \n
    aviasales -from LWN -to MOW -s 2018-04-28 -e 2018-05-03 -p 5200 \n
    """
    print('start at {} UTC'.format(
        dt.strftime(dt.utcfromtimestamp(int(dt.now().timestamp())), '%Y-%m-%d %H:%M:%S')
    ))

    # debug mode
    if debug:
        print('debug: mode on')
    else:
        pass

    # init parsers/db
    tickets_db = DBConnector(DATABASE_URL, echo=False)  # ('sqlite:///:memory:') or DATABASE_URL
    tickets_db.setup()
    print('ticket_db set up successful')

    # share group values between commands
    ctx.obj['DEBUG'] = debug or False
    ctx.obj['DB_instance'] = tickets_db


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--origin_airport', '-from', type=str, default='MOW',
              help='airport of departure. example: MOW')
@click.option('--destination_airport', '-to', type=str, default='LWN',
              help='airport of arrival. example: LWN')
@click.option('--start', '-s', type=str, default=dt.now().strftime('%Y-%m-%d'),
              help='date when your trip will starts')
@click.option('--end', '-e', type=str, default=(dt.now() + td(6)).strftime('%Y-%m-%d'),
              help='date when your trip will ends')
@click.option('--price', '-p', type=int, default=2000, help='maximum ticket price')
@click.pass_context
def aviasales(ctx, origin_airport, destination_airport, start, end, price):
    """Aviasales parser"""

    # download tickets
    try:
        print('aviasales parser starts')
        a = AviaSalesParser()
        tickets = a.get_data(origin_airport=origin_airport,
                             destination_airport=destination_airport,
                             depart_start=start,
                             depart_end=end,
                             price=price)
        print('collected tickets:', len(tickets))

    except Exception as e:
        print(e)

    # add tickets to DB
    if tickets:
        ctx.obj['DB_instance'].add_tickets(tickets)

    # send new tickets to Telegram channel
    new_tickets = ctx.obj['DB_instance'].get_new_tickets(price)

    if new_tickets:
        try:
            if ctx.obj['DEBUG']:
                [print(ticket) for ticket in new_tickets]
            else:
                # todo check telegram sending
                send(url=HEROKU_URL + URL_SUFFIX,
                     chat_id=CHAT_ID,
                     msg='\n'.join([str(ticket) for ticket in new_tickets]))
        except Exception:
            print('Send to telegram error: \n {}'.format(traceback.format_exc()))
        else:
            ctx.obj['DB_instance'].update_telegram_status(new_tickets)

    # exit
    ctx.obj['DB_instance'].remove_old_tickets()
    ctx.obj['DB_instance'].teardown()
    print('finish at {} UTC'.format(
        dt.strftime(dt.utcfromtimestamp(int(dt.now().timestamp())), '%Y-%m-%d %H:%M:%S')
    ))
    print('===============================')


if __name__ == "__main__":
    cli(obj={})

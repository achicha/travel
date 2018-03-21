from datetime import datetime as dt, timedelta as td
import click
from parsers.aviasales import AviaSalesParser

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
    click.echo('start')

    if debug:
        print('debug: mode on')
    else:
        pass

    # share group values between commands
    ctx.obj['DEBUG'] = debug or False
    print(ctx.obj['DEBUG'])


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

    try:
        a = AviaSalesParser()
        data = a.get_data(origin_airport=origin_airport,
                          destination_airport=destination_airport,
                          depart_start=start,
                          depart_end=end,
                          price=price)

        print(data)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    cli(obj={})


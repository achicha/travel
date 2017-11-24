"""
register our bot in telegram:
1. go to @BotFather
    - /start
    - /newbot
    - create name endswith "bot".
    - get unique toke like 311825528:AAE3r8V7iaIiXzJY_s0-9brG6JMWbT126qB
    - add bot to your telegram contacts
2. get bot's id and name:
    - id and first_name from page: api.telegram.org/bot<TOKEN>/getMe
3. get chat_id:
    - id from page://api.telegram.org/botXXXX:TOKEN/getUpdates
4. check. send your msg to bot.
    curl --header 'Content-Type: application/json' -X POST \
    --data '{"chat_id":"281724313","text":"your_message"}' \
    "https://api.telegram.org/bot311825528:AAE3r8V7iaIiXzJY_s0-9brG6JMWbT126qB/sendMessage"
5. example webhook:
    - https://habrahabr.ru/post/322078/
"""

import asyncio
import aiohttp
from aiohttp import web
import json
from telegram_bot.settings import my_chat_id, TOKEN


API_URL = 'https://api.telegram.org/bot%s/sendMessage' % TOKEN


async def handler(loop, data):
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        'chat_id': my_chat_id,
        'parse_mode': 'Markdown',
        'text': '\n'.join([str(i) for i in data])
    }
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.post(API_URL,
                                data=json.dumps(message),
                                headers=headers) as resp:
            try:
                assert resp.status == 200
            except BaseException:
                return web.Response(status=500)
    return web.Response(status=200)


if __name__ == '__main__':
    data = 'my_text_message'
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(handler(loop, data))
    except Exception as e:
        print('Error create server: %r' % e)
    finally:
        loop.close()

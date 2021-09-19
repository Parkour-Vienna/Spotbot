from discourse import Forum
from spotbot import Spotbot
import logging
import os


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('initializing forum connection')
    url = os.environ['SPOTBOT_URL']
    username = os.environ['SPOTBOT_USERNAME']
    token = os.environ['SPOTBOT_TOKEN']
    f = Forum(url,username,token)
    logging.info('testing connectivity')
    f.check_connection()
    bot = Spotbot(f)
    bot.run()

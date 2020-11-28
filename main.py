from discourse import Forum
from spotbot import Spotbot
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('initializing forum connection')
    f = Forum('http://beta.parkourvienna.at', 'Spotbot',
              '2d6a1397fafdb361d9f4e3236d14e8cb3c1418de93883cd53cf7ad34ffe932e1')
    logging.info('testing connectivity')
    f.check_connection()
    bot = Spotbot(f)
    bot.run()

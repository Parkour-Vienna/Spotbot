from discourse import Forum
from spotbot import Spotbot


if __name__ == '__main__':
    f = Forum('http://beta.parkourvienna.at', 'Spotbot',
              '2d6a1397fafdb361d9f4e3236d14e8cb3c1418de93883cd53cf7ad34ffe932e1')
    bot = Spotbot(f, 'starter.json')
    bot.run()

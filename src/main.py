from bottle import route, run, template
from datetime import datetime
@route('/')
def index(name='time'):
    dt = datetime.now()
    time = "{:%Y-%m-%d %H:%M:%S}".format(dt)
    return template(' <head> <h1> Welcome to MechatronicsLab </h1> </head> <br>    '
                    '<b> <h3> Raspberry Pi Thinks Today is : </h3>  <br> date/time : {{t}}</b>', t=time)
run(host='localhost', port=8080)
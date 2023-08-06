from exposer.exposer import Exposer
from exposer.actions import PathAction
from exposer.targets import Wsgi
from exposer.actions import CliAction
from exposer.targets import Cli
from wsgiref.simple_server import make_server


class app(object):
    cli = Exposer(action=CliAction, target=Cli)
    web = Exposer(action=PathAction, target=Wsgi)


class people:
    @staticmethod
    @app.web
    @app.cli
    def greetings(
        name=None, surname=None, greeting="Hello"
    ):
        print(
            "{}, {} {}".format(
                greeting,
                name.capitalize(),
                surname.capitalize(),
            )
        )


@app.web
@app.cli
def index():
    print("Welcome")


@app.cli
def run():
    APP = app.web.expose()
    app.web.rename("/index", "/")
    httpd = make_server("localhost", 8051, APP)
    import threading

    t = threading.Thread(None, httpd.serve_forever)
    t.start()
    import time

    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt as ki:
            httpd.shutdown()
            t.join()
            break


app.cli.expose()

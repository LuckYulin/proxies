from webapp import app
from config import API


def app_start():
    host, port = API
    app.run(host, port, True)


if __name__ == '__main__':
    app_start()
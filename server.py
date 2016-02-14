from mpos import app


def run_server():
    app.run(threaded=True)


if __name__ == '__main__':
    run_server()

import server

from mpos import manager
from app.migrations import dbmigrate, seeds


@manager.command
def runserver():
    server.run_server()


@manager.command
def migrate():
    dbmigrate.run_migration()


@manager.command
def seed():
    seeds.run_seed()


if __name__ == '__main__':
    manager.run()

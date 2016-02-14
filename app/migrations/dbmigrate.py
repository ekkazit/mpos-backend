from mpos import db


def run_migration():
    db.drop_all()
    db.create_all()
    print 'All table migrated'


if __name__ == '__main__':
    run_migration()

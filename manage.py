#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : manage.py
# Author: jixin
# Date  : 18-10-17
import os
from app import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db
from app.auth.models import User

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=app', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


@manager.command
def adduser(email, username, admin=False):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))


@manager.command
def runserver():
    app.run()


if __name__ == '__main__':
    manager.run()

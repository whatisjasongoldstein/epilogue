from __future__ import absolute_import

import os
from flask import Flask

from playhouse.flask_utils import FlaskDB

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, '../db/epilogue.sqlite')
DEBUG = False

# TODO: change and hide these
SECRET_KEY = os.environ['EPILOGUE_SECRET_KEY']  # Used by Flask to encrypt session cookie.
secret_webhook_uuid = os.environ['EPILOGUE_WEBHOOK_UUID']

app = Flask(__name__)
app.config.from_object(__name__)

db = FlaskDB(app)

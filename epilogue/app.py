from __future__ import absolute_import

import os
from flask import Flask

from playhouse.flask_utils import FlaskDB

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, '../db/epilogue.sqlite')
DEBUG = False

# TODO: change and hide these
SECRET_KEY = "Don't tell anyone!"  # Used by Flask to encrypt session cookie.
secret_webhook_uuid = "44ff110a-b3de-4722-814e-4da15f65b2ae"

app = Flask(__name__)
app.config.from_object(__name__)

db = FlaskDB(app)

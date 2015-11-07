from __future__ import absolute_import

import os
import warnings
from flask import Flask
from playhouse.flask_utils import FlaskDB
from werkzeug.contrib.cache import MemcachedCache

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, '../db/epilogue.sqlite')
DEBUG = False

SECRET_KEY = os.environ.get('EPILOGUE_SECRET_KEY', None)  # Used by Flask to encrypt session cookie.
secret_webhook_uuid = os.environ.get('EPILOGUE_WEBHOOK_UUID', None)

if not SECRET_KEY:
    warnings.warn("SECRET_KEY is not set. An insecure dev key will be used.")
    SECRET_KEY = "this-is-not-a-secret"

if not secret_webhook_uuid:
    warnings.warn("secret_webhook_uuid is not set. An insecure dev key will be used.")
    secret_webhook_uuid = "its-no-secret"


app = Flask(__name__)
app.config.from_object(__name__)

db = FlaskDB(app)

cache = MemcachedCache(['127.0.0.1:11211'])

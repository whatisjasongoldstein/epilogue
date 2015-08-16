from __future__ import absolute_import

from settings import app, db

from views import *
from webhooks import *
from assets import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
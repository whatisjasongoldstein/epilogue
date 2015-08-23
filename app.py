from __future__ import absolute_import

from epilogue.app import app, db
from epilogue.views import *
from epilogue.webhooks import *
from epilogue.assets import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
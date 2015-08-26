import sass
from flask.ext.assets import Environment, Bundle, register_filter
from webassets_libsass import LibSass

from .app import app

register_filter(LibSass)

assets = Environment(app)
assets.versions = 'hash'
assets.url = app.static_url_path

styles = Bundle('css/*.scss', filters="libsass", output='gen/styles.css')

assets.register("styles", styles)

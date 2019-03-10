"""
# encoding:utf-8
import os

from flask import Flask, redirect, url_for
from gallery.views import gallery
import settings


ROOT_DIR = os.path.dirname(__file__)

UPLOAD_DIR = os.path.join(ROOT_DIR, 'uploads')
UPLOAD_ALLOWED_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'gif',
)


app = Flask(__name__)
app.register_blueprint(gallery, url_prefix='/static')
app.config['GALLERY_ROOT_DIR'] = settings.GALLERY_ROOT_DIR

@app.route('/')
def index():
    return redirect(url_for('static.show_gallery'))

if __name__ == '__main__':
    app.logger.info('Listening on http://localhost:8000')
    app.run(port=8000, debug=True)


"""
import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
        return """Hello from Python!
        <img src="/static/atul3.jpg">
        """

if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)




from flask import Flask
app = Flask(__name__, template_folder=r'flask/templates',static_folder=r'flask/static')

import cryptoTracker.flask.views
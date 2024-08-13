from flask import Flask

def init_app():
    """Construct core Flask application."""
    app = Flask(__name__, instance_relative_config=False , template_folder=r'flask/templates',static_folder=r'flask/static')
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        import cryptoTracker.flask.views

                # Import Dash application
        from cryptoTracker.flask.dash import init_dashboard
        app = init_dashboard(app)

        return app
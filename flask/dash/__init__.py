from dash import Dash
from flask import Flask

def init_dashboard(app : Flask):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=app,
        routes_pathname_prefix='/dashboard/',
        external_stylesheets=[
           '/home/zionunix/Repos/cryptoTracker/cryptoTracker/flask/static/css/style.css',
        ]
    )
    from .data import token_data

    from .layout import load_dashboard_layout
    dash_app.layout = load_dashboard_layout()

    from .callbacks import init_callbacks
    init_callbacks(dash_app=dash_app)

    return dash_app.server
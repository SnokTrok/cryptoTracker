from flask import render_template , jsonify , request , Response , redirect
from markdown import markdown
from cryptoTracker.db.utils import init_pg_db
from cryptoTracker.flask.dash.figures.utils import (
    generate_price_history_charts
)

from flask import current_app as app
"""
    Contains our entry point or our Flask web application
"""

@app.route('/')
def entry_point():
    global token_id
    global token_html
    token_id = 1
    template = "main.html"
    # build display for these tokens....
    return render_template(template , devlog=convert_md_to_html('/home/zionunix/Repos/cryptoTracker/cryptoTracker/devlog/entry1.md'))


@app.route('/open-dashboard', methods=['POST'])
def redirect_to_dashboard():
    return redirect('/dashboard/')



def convert_md_to_html(file : str):
    with open(file , 'r') as f:
        md_raw = f.read()
    html = markdown(md_raw)
    return html


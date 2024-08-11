from flask import render_template , jsonify , request , Response
from cryptoTracker import app
from cryptoTracker.db.utils import init_pg_db
from cryptoTracker.flask.figures.utils import (
    generate_token_info_html , generate_price_history_charts
)
"""
    Contains our entry point or our Flask web application
"""
def generate_graph_htmls():
    global token_id
    global token_html
    candle_graph , line_graph = generate_price_history_charts(token_id=token_id)
    candle_graph = candle_graph.to_html(full_html=False)
    line_graph = line_graph.to_html(full_html=False)

    return line_graph , candle_graph

def render_main_template():
    global token_id
    global token_html
    template = "main.html"
    print(token_id)
    token_html = generate_token_info_html(selected_token_id=token_id)
    line_graph , candle_graph = generate_graph_htmls()
    return render_template(template, token_html=token_html , fig_candlestick=candle_graph, fig_linegraph=line_graph)

@app.route('/')
def entry_point():
    global token_id
    global token_html
    token_id = 1
    init_pg_db()
    # build display for these tokens....
    return render_main_template()



# region -----------------BUTTONS---------------------

@app.route('/change-token',methods=['POST'])
def change_token():
    """
        Change our token_id desired view
    """
    global token_id
    new_token_id = request.form.get('token_id')

    try:
        data = request.get_json()
        if data:
            new_token_id = data.get('token_id')
    except:
        # most likely not type application/json
        pass

    if new_token_id == None:
        print("Failed to find token_id from request")
        return Response(status=204)
    
    if new_token_id == token_id:
        return Response(status=204)

    token_id = new_token_id
    return render_main_template()
    



@app.route('/change-periodicity',methods=['POST'])
def change_periodicity():
    """
        Switch from monthly / weekly / daily rollup views on graphs
    """
    token_id = request.form.get('token_id')
    periodicity = request.form.get('periodicity')

    try:
        data = request.get_json()
        if data:
            token_id = data.get('token_id')
            periodicity = data.get('periodicity')
    except:
        # most likely not type application/json
        pass

    resp = {
        'token_id' : token_id,
        'periodicity' : periodicity
    }
    return jsonify(resp)


 # endregion.  ----------------------------------------

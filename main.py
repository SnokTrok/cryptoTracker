from cryptoTracker import init_app
from cryptoTracker.db.utils import init_pg_db , get_pg_db

app = init_app()

if __name__ == '__main__' : 
    init_pg_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
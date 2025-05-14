from app import create_app, db
from app.database.db import init_db

app = create_app()

with app.app_context():
    init_db(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000) 
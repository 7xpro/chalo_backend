from flask import Flask
from sqlalchemy import text
from app.schema.user_schema import ma
from app.database.db import db, init_db
from app.config import config
from app.routes.user import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    ma.init_app(app)
    init_db(app) 
   

    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print("Database connection successful")
        except Exception as e:
            print(f"Error occurred while testing database connection: {e}")

    app.register_blueprint(user_bp, url_prefix='/user')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
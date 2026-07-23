from app.database.db import db
from app.models.user import User
from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ("password_hash",)

    password = fields.String(
        required=True,
        load_only=True,
        data_key="password",
        attribute="password_hash",
    )
        
    
user_schema = UserSchema()            # single user
users_schema = UserSchema(many=True)  # list of users
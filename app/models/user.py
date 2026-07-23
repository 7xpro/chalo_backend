from app.database.db import db
from datetime import datetime

class User(db.Model):
    
    __tablename__ ="users"
    
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False,unique=True)
    password_hash=db.Column(db.String(100),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.now)
    updated_at=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

    
    def __repr__(self):
        return f"<User {self.name}>"
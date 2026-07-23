from flask import request, jsonify
import app.schema.user_schema as UserSchema
from app.database.db import db
from sqlalchemy.exc import IntegrityError, OperationalError
import bcrypt




class user_controller:

    @staticmethod
    def create_user():
        data = request.get_json() or {}
        print(f"Received data: {data}")
        error = UserSchema.user_schema.validate(data)
        if error:
            print(f"Validation error: {error}")
            return jsonify({"error": error}), 400
        
        plain_password = data.get("password")
        if not plain_password:
            return jsonify({"error": "Password is required"}), 400
        
        
        hashed_password = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")


        data["password"] = hashed_password
        
        new_user = UserSchema.user_schema.load(data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email already exists"}), 409
        except OperationalError as exc:
            db.session.rollback()
            return jsonify({"error": f"Database schema error: {exc.orig}"}), 500

        return jsonify({"message": "User created successfully"}), 201

    
    
    @staticmethod
    def login_user():
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = UserSchema.User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
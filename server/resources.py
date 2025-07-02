from flask_restful import Resource
from flask import request, session
from server.config import db
from server.models import User, Recipe
from sqlalchemy.exc import IntegrityError

class Signup(Resource):
    def post(self):
        json = request.get_json()
        try:
            user = User(
                username=json.get('username'),
                image_url=json.get('image_url'),
                bio=json.get('bio')
            )
            user.password_hash = json.get('password')
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return user.to_dict(only=('id', 'username', 'image_url', 'bio')), 201
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = db.session.get(User, user_id)
            if user:
                return user.to_dict(only=('id', 'username', 'image_url', 'bio')), 200
        return {'error': 'Unauthorized'}, 401

class Login(Resource):
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(only=('id', 'username', 'image_url', 'bio')), 200
        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session.pop('user_id', None)
            return {}, 204
        return {'error': 'Unauthorized'}, 401

class RecipeIndex(Resource):
    def get(self):
        if session.get('user_id'):
            recipes = Recipe.query.filter_by(user_id=session['user_id']).all()
            return [recipe.to_dict(only=('id', 'title', 'instructions', 'minutes_to_complete', 'user')) for recipe in recipes], 200
        return {'error': 'Unauthorized'}, 401

    def post(self):
        if session.get('user_id'):
            json = request.get_json()
            try:
                recipe = Recipe(
                    title=json.get('title'),
                    instructions=json.get('instructions'),
                    minutes_to_complete=json.get('minutes_to_complete'),
                    user_id=session['user_id']
                )
                db.session.add(recipe)
                db.session.commit()
                return recipe.to_dict(only=('id', 'title', 'instructions', 'minutes_to_complete', 'user')), 201
            except ValueError as e:
                db.session.rollback()
                return {'errors': [str(e)]}, 422
        return {'error': 'Unauthorized'}, 401
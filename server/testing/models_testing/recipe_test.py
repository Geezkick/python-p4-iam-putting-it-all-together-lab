from server.config import db
from server.models import User, Recipe

def test_recipe_creation(client):
    with client:
        user = User(username='testuser', image_url='https://example.com/image.jpg', bio='Test bio')
        user.password_hash = 'testpassword'
        db.session.add(user)
        db.session.commit()

        recipe = Recipe(
            title='Test Recipe',
            instructions='This is a test recipe with more than 50 characters to satisfy the validation requirement.',
            minutes_to_complete=30,
            user_id=user.id
        )
        db.session.add(recipe)
        db.session.commit()

        assert recipe.id is not None
        assert recipe.title == 'Test Recipe'
        assert recipe.user_id == user.id
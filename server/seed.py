from app import app, db
from models import User, Recipe

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(username='testuser', image_url='http://example.com/image.jpg', bio='Test bio')
    user.password = 'password123'
    db.session.add(user)
    db.session.commit()

    recipe = Recipe(
        title='Test Recipe',
        instructions='This is a test recipe with more than 50 characters to satisfy the constraint.',
        minutes_to_complete=30,
        user_id=user.id
    )
    db.session.add(recipe)
    db.session.commit()

    print("Database seeded successfully!")
from app import create_app, db
from app.models import User  # Import your User model

app = create_app()

with app.app_context():
    db.create_all()  # Create all tables defined in your models
    print("Tables created successfully!")
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

# Create the Flask app and push the application context
app = create_app()
app.app_context().push()

# Check if the admin user already exists
admin_user = User.query.filter_by(Username='admin').first()

if admin_user:
    # Update the admin user's password
    admin_user.Password = generate_password_hash('admin123')  # Set a new password
    db.session.commit()
    print("Admin user updated successfully!")
else:
    # Create an admin user
    admin_user = User(
        Username='admin',  # Admin username
        Password=generate_password_hash('admin123'),  # Admin password (hashed)
        Role='Admin'  # Admin role
    )

    # Add the user to the database
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created successfully!")


# Check if the admin user already exists
admin_user = User.query.filter_by(Username='admin').first()

if not admin_user:
    # Create an admin user
    admin_user = User(
        Username='admin',  # Admin username
        Password=generate_password_hash('admin123'),  # Admin password (hashed)
        Role='Admin'  # Admin role
    )

    # Add the user to the database
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created successfully!")
else:
    print("Admin user already exists. Skipping creation.")


    # Check if the admin user already exists
admin_user = User.query.filter_by(Username='admin').first()

if admin_user:
    # Delete the existing admin user
    db.session.delete(admin_user)
    db.session.commit()
    print("Existing admin user deleted.")

# Create a new admin user
admin_user = User(
    Username='admin',  # Admin username
    Password=generate_password_hash('admin123'),  # Admin password (hashed)
    Role='Admin'  # Admin role
)

# Add the user to the database
db.session.add(admin_user)
db.session.commit()
print("Admin user created successfully!")

from werkzeug.security import generate_password_hash

from database.auth_db import get_connection


name = "HR Admin"
email = "admin@hrassistant.com"
password = "Admin@123"


connection = get_connection()

existing_user = connection.execute(
    "SELECT id FROM users WHERE email = ?",
    (email,)
).fetchone()

if existing_user:
    print("Admin account already exists.")
else:
    connection.execute(
        """
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            generate_password_hash(password),
            "admin"
        )
    )

    connection.commit()
    print("Admin account created successfully.")

connection.close()
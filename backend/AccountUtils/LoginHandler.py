import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from SQLUtils.SQLConnect import connect_with_connector

def verify_login(username: str, password: str) -> dict | None:
    """
    Verifies user credentials against the database.

    Args:
        username: The username provided by the user.
        password: The plaintext password provided by the user.

    Returns:
        A dictionary containing account info (id, username) if successful,
        otherwise None.
    """
    engine = connect_with_connector()
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            # 1. Prepare a SQL statement to securely fetch the user's data
            # Using text() with parameters prevents SQL injection.
            query = text("SELECT id, player_name, password FROM players WHERE player_name = :username_param")
            
            # 2. Execute the query
            result = session.execute(query, {"username_param": username}).fetchone()

            # 3. If no user is found, return None
            if result is None:
                print(f"Login failed: User '{username}' not found.")
                return None

            # 4. Map the database row to variables
            user_id, db_username, hashed_password = result
            
            # The hashed password from the DB is likely a string, needs to be bytes
            hashed_password_bytes = hashed_password.encode('utf-8')
            password_bytes = password.encode('utf-8')

            # 5. Use bcrypt to compare the provided password with the stored hash
            if bcrypt.checkpw(password_bytes, hashed_password_bytes):
                # Passwords match! Prepare the account info to return.
                account_info = {
                    "id": user_id,
                    "username": db_username
                }
                print(f"Login successful for user: {username}")
                return account_info
            else:
                # Passwords do not match
                print(f"Login failed: Invalid password for user '{username}'.")
                return None
        
        except Exception as e:
            print(f"An error occurred during login verification: {e}")
            return None

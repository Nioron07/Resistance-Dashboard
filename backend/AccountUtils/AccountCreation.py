import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, exc
from SQLUtils.SQLConnect import connect_with_connector
def create_account(username: str, password: str) -> dict:
    """
    Creates a new user account, initializing all stats to 0.

    Args:
        username: The desired username.
        password: The plaintext password for the new account.

    Returns:
        A dictionary with a success status and a message.
    """
    engine = connect_with_connector()
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            # 1. Check if the username already exists
            check_query = text("SELECT id FROM players WHERE player_name = :username_param")
            existing_user = session.execute(check_query, {"username_param": username}).first()

            if existing_user:
                return {"success": False, "message": "Username is already taken."}

            # 2. Hash the password
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt(rounds=7)
            hashed_password = bcrypt.hashpw(password_bytes, salt)

            # 3. Insert the new user with all stats initialized to 0
            # The 'player_name' column will also be set to the username by default.
            insert_query = text(
                """
                INSERT INTO players (
                    password, player_name, total_games, favorable_missions,
                    unfavorable_missions, favorable_votes, unfavorable_votes,
                    favorable_plot_cards, unfavorable_plot_cards, favorable_teams,
                    unfavorable_teams, players_fooled, players_not_fooled,
                    found_as_commander, picked_commander, games_won, failed_votes,
                    total_score, times_as_resistance, times_as_spy, games_lost
                ) VALUES (
                    :password, :username, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                )
                """
            )
            session.execute(
                insert_query,
                {
                    "username": username,
                    "password": hashed_password.decode('utf-8'),
                    "player_name": username
                }
            )

            # 4. Commit the transaction to save the changes
            session.commit()

            return {"success": True, "message": "Account created successfully."}

        except exc.SQLAlchemyError as e:
            session.rollback()  # Roll back the transaction on error
            print(f"Database error during account creation: {e}")
            return {"success": False, "message": "A database error occurred."}
        except Exception as e:
            print(f"An unexpected error occurred during account creation: {e}")
            return {"success": False, "message": "An unexpected error occurred."}

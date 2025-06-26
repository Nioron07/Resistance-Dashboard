from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, exc
from SQLUtils.SQLConnect import connect_with_connector

def get_account_details(username: str) -> dict | None:
    """
    Retrieves the full statistical profile for a given user.

    Args:
        username: The username of the player to look up.

    Returns:
        A dictionary containing all account stats if the user is found,
        otherwise None.
    """
    engine = connect_with_connector()
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            # We select all columns to build the full profile
            query = text("SELECT * FROM players WHERE player_name = :username_param")
            
            # .mappings() returns a Row object that can be treated like a dict
            result = session.execute(query, {"username_param": username}).mappings().fetchone()

            if result is None:
                print(f"No account found for user: {username}")
                return None

            # Create a dictionary from the result, excluding sensitive/unwanted keys
            account_details = {key: value for key, value in result.items() if key not in ['password', 'player_name']}
            
            return account_details

        except exc.SQLAlchemyError as e:
            print(f"Database error while fetching account details: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching account details: {e}")
            return None

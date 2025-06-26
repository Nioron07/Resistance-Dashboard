from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
from AccountUtils.LoginHandler import verify_login
from AccountUtils.AccountCreation import create_account
from AccountUtils.AccountHandler import get_account_details
from dotenv import load_dotenv # 1. Import the library

load_dotenv() # 2. Load the .env file
# 1. Initialize the Flask application
app = Flask(__name__)

# 2. Enable CORS
# This will allow requests from your Nuxt frontend (http://localhost:3000)
# to access the API.
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# 3. Define the login endpoint
@app.route('/login', methods=['POST'])
def login():
    """
    Handles the login request by calling the login handler.
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    account_info = verify_login(username, password)

    if account_info:
        return jsonify(account_info), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401

# 4. Define the create account endpoint
@app.route('/create_account', methods=['POST'])
def create_account_route():
    """
    Handles the account creation request.
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    result = create_account(username, password)

    if result["success"]:
        return jsonify({"msg": result["message"]}), 201 # 201 Created
    else:
        status_code = 409 if "taken" in result["message"] else 400
        return jsonify({"msg": result["message"]}), status_code

@app.route('/getAccountInfo', methods=['GET'])
def get_account_info_route():
    """
    Retrieves account statistics based on a username from query parameters.
    """
    # 1. Get username from query parameters (e.g., /getAccountInfo?username=test)
    username = request.args.get('username')

    # 2. Validate that the username parameter was provided
    if not username:
        return jsonify({"msg": "Missing username query parameter"}), 400

    # 3. Call the handler function
    account_details = get_account_details(username)

    # 4. Return the data or a 404 error if not found
    if account_details:
        return jsonify(account_details), 200
    else:
        return jsonify({"msg": f"Account not found for username: {username}"}), 404
# 5. Standard entry point to run the application
if __name__ == '__main__':
    app.run(debug=True, port=8080)


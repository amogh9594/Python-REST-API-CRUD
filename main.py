import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
		
@app.route('/add', methods=['POST'])
def add_user():
	"""Adds a new user to the database with hashed password.
	Parameters:
	- No parameters are directly passed, but expects 'name', 'email', and 'pwd' in the request JSON body.
	Returns:
	- response (JSON): A JSON response with a success status code on successful addition, or calls not_found() on failure.
	Processing Logic:
	- Hashes the password before storing it in the database for security reasons.
	- Commits the transaction to the database for persistence.
	- Encloses database operations in a try-except block to handle exceptions gracefully.
	- Closes database connection and cursor in the finally block to ensure resources are freed."""
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


		
@app.route('/users')
def users():
	"""Fetches and returns all users from the database.
	Parameters:
	None
	Returns:
	- response object: A response object with all users as JSON and HTTP status code 200 on success.
	Processing Logic:
	- Utilizes a MySQL connection to fetch user data.
	- Employs a try-except block to handle any exceptions that might occur during database operations.
	- Ensures the closure of database cursor and connection in the finally block."""
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<int:id>')
def user(id):
	"""Fetch user information from the database using a given user ID.
	Parameters:
	- id (int or str): The user ID for which to fetch information.
	Returns:
	- Flask Response object: JSON representation of user data and status code.
	Processing Logic:
	- A database connection is created and a cursor with a DictCursor to return the data as a dictionary.
	- A SELECT query is executed with the user ID to fetch a single user's data.
	- If an exception occurs, it is printed to the console.
	- The database connection and cursor are closed in the finally block to ensure resources are released."""
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/update', methods=['POST'])
def update_user():
	"""Update user details in the database.
	Parameters:
	- None: Function extracts parameters from a JSON request.
	Returns:
	- Response: JSON response indicating success or failure.
	Processing Logic:
	- Validates that the required parameters (id, name, email, pwd) are provided in the POST request.
	- Hashes the password before saving it to the database.
	- Updates the user information in the 'tbl_user' table using the provided id.
	- Handles exceptions and ensures database connection is closed."""
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']		
		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>')
def delete_user(id):
	"""Deletes a user from the database by their user ID.
	Parameters:
	- id (int): The unique identifier of the user to be deleted.
	Returns:
	- Response object: A JSON response indicating the result of the operation, including status code.
	Processing Logic:
	- The function establishes a connection to the MySQL database.
	- It uses a DELETE SQL query to remove the user record.
	- Commits the change to the database and closes the connection."""
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    """Returns a 404 Not Found response with the URL that was requested.
    Parameters:
        - error (optional): The error object, not used in this function.
    Returns:
        - Response: A Response object with a JSON body and a 404 status code.
    Processing Logic:
        - The function constructs a JSON response containing the URL that could not be found.
        - It is assumed the request context is available where this function is called for access to the request.url."""
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
		
if __name__ == "__main__":
    app.run()
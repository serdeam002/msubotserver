from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import requests
import os  # Import the 'os' module

app = Flask(__name__)

# Replace 'mysql://username:password@hostname:port/database' with your actual connection string
connection_string = 'mysql://pm8cfhicxbsdjtb8gyfc:pscale_pw_D44uw2QeL5oyqhRHiO8DN4ceTdIFz5dIKlzbd01GG30@aws.connect.psdb.cloud:3306/msubotdb?ssl_ca=cacert.pem&ssl=true'
engine = create_engine(connection_string)

# Heroku app URL
heroku_app_url = 'https://msubotserver-8a9bb5aee729.herokuapp.com'

@app.route('/fetchData', methods=['GET'])
def fetch_data():
    try:
        # Use the PlanetScale connection to execute the query
        query = text('SELECT * FROM serials')  # Replace 'your_table' with your actual table name
        with engine.connect() as connection:
            result = connection.execute(query)

        # Return the result as JSON
        return jsonify(result.fetchall())
    except Exception as e:
        print(f"Error fetching data from PlanetScale: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/sendData', methods=['POST'])
def send_data():
    try:
        # Assuming request data is JSON
        data_to_send = request.get_json()

        # Make a POST request to the Heroku app
        heroku_response = requests.post(f"{heroku_app_url}/receiveData", json=data_to_send)

        return jsonify({'message': 'Data sent to Heroku successfully', 'herokuResponse': heroku_response.json()})
    except Exception as e:
        print(f"Error sending data to Heroku: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Use the 'PORT' environment variable provided by Heroku for dynamic port binding
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use port 5000 if not provided
    app.run(debug=False, port=port)

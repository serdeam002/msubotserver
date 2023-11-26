from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import requests

app = Flask(__name__)

# Replace 'mysql://username:password@hostname:port/database' with your actual connection string
connection_string = 'mysql://24my8fz00ty91mboo88m:pscale_pw_1WZLu373165m46cl7KPy988hWuMP7aCDtGUocegwLHU@aws.connect.psdb.cloud:3306/msubotdb'
engine = create_engine(connection_string)

# Heroku app URL
heroku_app_url = 'YOUR_HEROKU_APP_URL'

@app.route('/fetchData', methods=['GET'])
def fetch_data():
    try:
        # Use the PlanetScale connection to execute the query
        query = text('SELECT * FROM serials')
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

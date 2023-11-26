import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Replace 'YOUR_PLANETSCALE_API_KEY', 'YOUR_PLANETSCALE_ORG', and 'YOUR_PLANETSCALE_DB' with your actual values
planet_scale_api_key = 'pscale_tkn_AUfnc8OpiwAZx7aA7cuEjY8pgLzddK8r-mg7p_MnXj8'
organization = 'thanawanphansa2020'
database = 'msubotdb'

# PlanetScale API base URL
planet_scale_api_url = f'https://api.planetscale.com/v1/organizations/{organization}/databases/{database}'

# Set the API key in the headers
headers = {
    'Authorization': f'Bearer {planet_scale_api_key}',
    'Content-Type': 'application/json',
}

@app.route('/fetchData', methods=['GET'])
def fetch_data():
    try:
        # Example GET request to fetch data
        response = requests.get(f'{planet_scale_api_url}/tables/serials', headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': f'Failed to fetch data. Status Code: {response.status_code}'}), response.status_code

    except Exception as e:
        print(f"Error fetching data from PlanetScale: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Add other routes and functions as needed

if __name__ == '__main__':
    app.run(debug=False)

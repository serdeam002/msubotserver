import MySQLdb
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
load_dotenv()
mysql = MySQL(app)
CORS(app)

# Create a MySQL connection
db = MySQLdb.connect(
    host="aws.connect.psdb.cloud",
    user="w5nl2ipnvgso7hgbatjb",
    passwd="pscale_pw_LXxna9Dgjy7P9e3828jhPUi8Gtx7W0RzCxaPaUMU1GH",
    db="msubotdb",
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY",
    ssl={
        "ca": "cacert.pem"
    }
)
cursor = db.cursor()

@app.route('/api/verify_serial', methods=['GET'])
def verify_serial():
    try:
        user_serial = request.args.get('serial')

        # Check if the serial exists in the database
        query = "SELECT * FROM computer_usage WHERE serial = %s"
        cursor.execute(query, (user_serial,))
        result = cursor.fetchone()

        if result:
            # Check if the serial in computer_usage matches the one entered by the user
            if result[2] == user_serial:
                # Serials match, open the program
                return jsonify({"error": "Serial is already in use.\n\nซีเรียลถูกใช้งานแล้ว"})

            else:
                # Serials don't match, proceed to insert the serial
                return insert_serial(user_serial)
        else:
            # Serial not found, proceed to insert the serial
            return insert_serial(user_serial)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/insert_serial', methods=['POST'])
def insert_serial(user_serial):
    try:
        client_mac_address = request.headers.get('Client-MAC-Address')
        # Check if the serial exists in the database
        query = "SELECT * FROM serials WHERE serial = %s"
        cursor.execute(query, (user_serial,))
        result = cursor.fetchone()

        if result:
            # Serial exists, store data in computer_usage table

            insert_query = "INSERT INTO computer_usage (mac_address, serial, is_serial_used) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (client_mac_address, user_serial, True))
            db.commit()

            # Display success message
            return jsonify({"message": "Serial successfully used. Program is opening.\n\nซีเรียลสำเร็จแล้วโปรแกรมกำลังเปิด"})
        else:
            # Display error message for incorrect serial
            return jsonify({"error": "The serial is invalid!.\n\nซีเรียลไม่ถูกต้อง"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/computer_usage', methods=['GET'])
def check_computer_usage_server():
    try:

        # Get the client's MAC address from the request headers
        client_mac_address = request.headers.get('Client-MAC-Address')

        # Check if the current computer has used the serial before
        query = "SELECT * FROM computer_usage WHERE mac_address = %s"
        cursor.execute(query, (client_mac_address,))
        result = cursor.fetchone()
        print(f"Debug: Found result for MAC address {client_mac_address}: {result}")
        if result:
            # Display message for a computer already using the serial
            return jsonify({"message": "This computer already uses serial.\n\nคอมพิวเตอร์เครื่องนี้ใช้ซีเรียลแล้ว"})
        else:
            return jsonify({"error": "This computer is not running serial yet."})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

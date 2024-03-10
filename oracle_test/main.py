import oracledb
from flask import Flask, jsonify

un = 'ADMIN'
cs = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.eu-madrid-1.oraclecloud.com))(connect_data=(service_name=g73db8b01b7e944_capstonedb2_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'
pw = 'Capstone2024'

app = Flask(__name__)

@app.route('/')
def home():
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            sql = """select sysdate from dual"""
            for r in cursor.execute(sql):
                print(r)
                return jsonify(r)


if __name__ == '__main__':
    app.run(debug=True)

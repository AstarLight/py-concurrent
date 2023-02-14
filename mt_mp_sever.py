from flask import request, jsonify, Flask
import json
import gevent
from base_test import query_user_name, query_user_school, query_user_skills
from mt_test import mt_func

app = Flask(__name__)

@app.route('/query_user_info', methods=["GET"])
def query_user_info() :
    uid = request.args.get("uid")

    user_info = mt_func(uid)

    return jsonify(user_info)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=9998, processes=True)

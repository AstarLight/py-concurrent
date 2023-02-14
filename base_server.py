from flask import request, jsonify, Flask
import json
import gevent
from base_test import query_user_name, query_user_school, query_user_skills

app = Flask(__name__)

@app.route('/query_user_info', methods=["GET"])
def query_user_info() :
    uid = request.args.get("uid")

    school = query_user_school(uid)
    name = query_user_name(uid)
    skills = query_user_skills(uid)

    user_info = {}
    user_info["uid"] = uid
    user_info["school"] = school
    user_info["name"] = name
    user_info["skills"] = skills

    return jsonify(user_info)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=9999)

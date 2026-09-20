# app/utils/response.py
from flask import jsonify


def ok(data=None, msg="ok", code=0):
    return jsonify(code=code, msg=msg, data=(data if data is not None else {}))


def fail(msg="失败", code=4000, status=400):
    from flask import jsonify
    return jsonify(code=code, msg=msg), status
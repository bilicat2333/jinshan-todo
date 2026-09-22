# app/utils/response.py
from flask import jsonify


def ok(data=None, msg="ok", code=0):
    return jsonify(code=code, msg=msg, data=(data if data is not None else {}))


def fail(msg="失败", code=4000, status=400):
    # 失败响应同样补齐 data 字段，保持接口契约始终是 {code, msg, data}
    return jsonify(code=code, msg=msg, data=None), status

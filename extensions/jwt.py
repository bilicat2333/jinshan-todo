from flask import jsonify
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_jwt(app):
    """把 JWTManager 绑定到应用，并注册鉴权失败回调。

    flask-jwt-extended 默认自己产生鉴权失败的响应，响应体只有 msg 字段，
    不会走 app.errorhandler(401)，前端因此拿不到 code=4401，
    "token 过期自动回登录页"的逻辑就失效了。下面把几类失败收敛成统一格式。
    """
    jwt.init_app(app)

    def _unauthorized(msg: str):
        return jsonify(code=4401, msg=msg, data=None), 401

    @jwt.unauthorized_loader                 # 没带 Authorization 请求头
    def missing_token(reason):
        return _unauthorized("未登录：缺少 Authorization 请求头")

    @jwt.expired_token_loader                # token 已过期
    def expired_token(jwt_header, jwt_payload):
        return _unauthorized("登录已过期，请重新登录")

    @jwt.invalid_token_loader                # 签名错误 / 格式损坏
    def invalid_token(reason):
        return _unauthorized("token 无效，请重新登录")

    @jwt.revoked_token_loader                # token 已被撤销
    def revoked_token(jwt_header, jwt_payload):
        return _unauthorized("token 已失效，请重新登录")

    @jwt.needs_fresh_token_loader            # 需要二次验证的接口
    def needs_fresh_token(jwt_header, jwt_payload):
        return _unauthorized("请先完成身份二次验证")

    return jwt

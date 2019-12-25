from flask import Blueprint, request, redirect, url_for, make_response, abort
from flask import current_app as app
from linebot.exceptions import InvalidSignatureError
from .. import linebot, webhook

blueprint = Blueprint('auth_blueprint', __name__)

@blueprint.route('/callback', methods=['POST'])
def linebot_auth():
    if 'X-Line-Signature' not in request.headers:
        return make_response("Bad request", 400)
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text = True)
    app.logger.info("Request body: %s", body)

    try:
        webhook.handle(body, signature) 
    except InvalidSignatureError as e:
        # TODO: Make this kind of information output to log system
        print("Invalid Signature:", str(e))
        abort(400)

    return 'OK'

import logging
from flask import Flask, request, Response
from config import API_KEY
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.messages import VideoMessage
from viberbot.api.viber_requests import ViberUnsubscribedRequest


app = Flask(__name__)
viber = Api(BotConfiguration(
    name='TrainingPythonViberBot',
    avatar='http://site.com/avatar.jpg',
    auth_token=API_KEY
))


@app.route('/', methods=['POST'])
def incoming():
    logging.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


# def set_webhook(viber):
#     viber.set_webhook(f'https://viberbot8.herokuapp.com:{str(port)}/')


if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(port=8080, debug=True)

# if __name__ == "__main__":
#     scheduler = sched.scheduler(time.time, time.sleep)
#     scheduler.enter(5, 1, set_webhook, (viber,))
#     t = threading.Thread(target=scheduler.run)
#     t.start()
#     context = ('server.crt', 'server.key')
#
#     app.run(host='0.0.0.0', port=port, debug=True, ssl_context=context)

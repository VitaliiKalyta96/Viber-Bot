import logging
from flask import Flask, request, Response
import random

from config import API_KEY
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages import ContactMessage, PictureMessage, VideoMessage, URLMessage, StickerMessage, RichMediaMessage
from viberbot.api.messages.data_types.contact import Contact
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

import viber_message
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest


app = Flask(__name__)
viber = Api(BotConfiguration(
    name='TrainingPythonViberBot',
    avatar='http://site.com/avatar.jpg',
    auth_token=API_KEY
))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

text_message = TextMessage(text="Hello!")
contact = Contact(name="Viber user", phone_number="0123456789")
contact_message = ContactMessage(contact=contact)
picture_message = PictureMessage(text="Check this", media="https://res.cloudinary.com/dtpgi0zck/image/upload/s--zOSmBEhk--/c_fit,h_580,w_860/v1/EducationHub/photos/pebble-beach.jpg")
video_message = VideoMessage(media="https://www.youtube.com/", size=4324)
url_message = URLMessage(media="https://www.youtube.com/")
stc_message = StickerMessage(sticker_id=40104)
stc_message_1 = StickerMessage(sticker_id=40100)
stc_message_2 = StickerMessage(sticker_id=40113)
stc_message_3 = StickerMessage(sticker_id=40138)
stc_message_4 = StickerMessage(sticker_id=40137)
coincidence = [text_message, contact_message, picture_message, url_message, stc_message, stc_message_1, stc_message_2, stc_message_3, stc_message_4]


@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
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
        # lets return difference random message back
        viber.send_messages(viber_request.sender.id, [
            random.choice(coincidence)
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="Welcome!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


# def set_webhook(viber):
#     viber.set_webhook(f'https://viberbot8.herokuapp.com:{str(port)}/')


if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    # app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=context)
    app.run(port=8080)

# if __name__ == "__main__":
#     scheduler = sched.scheduler(time.time, time.sleep)
#     scheduler.enter(5, 1, set_webhook, (viber,))
#     t = threading.Thread(target=scheduler.run)
#     t.start()
#     context = ('server.crt', 'server.key')
#
#     app.run(host='0.0.0.0', port=port, debug=True, ssl_context=context)
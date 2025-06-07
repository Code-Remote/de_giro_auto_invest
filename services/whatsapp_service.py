import os

from whatsapp import WhatsApp, Message


class WhatsAppService:
    def __init__(self):
        self.messenger = WhatsApp(os.environ.get('WHATSAPP_TOKEN'),
                                  phone_number_id=os.environ.get('WHATSAPP_PHONE_NUMBER_ID'))

    def send_message(self, message):
        message = Message(instance=self.messenger, content=message, to=os.environ.get('WHATSAPP_PHONE_NUMBER_RECEIVER'))
        message.send()

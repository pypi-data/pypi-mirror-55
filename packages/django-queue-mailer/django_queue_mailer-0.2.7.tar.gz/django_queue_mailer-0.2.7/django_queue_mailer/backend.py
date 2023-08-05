import logging
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend
from django_queue_mailer.models import Queue
from django.core.files.base import ContentFile


logger = logging.getLogger(__name__)


class DbBackend(BaseEmailBackend):
    def send_messages(self, email_messages, app=None):
        num_sent = 0
        for message in email_messages:

            queue = Queue()
            queue.subject = message.subject
            queue.to_address = ', '.join(message.to)
            queue.bcc_address = ', '.join(message.bcc)
            queue.reply_to = ', '.join(message.reply_to)
            queue.from_address = message.from_email
            queue.content = message.body

            # Attach html aletrnative ...
            if hasattr(message, 'alternatives'):
                logger.debug(message.alternatives)
                for alt in message.alternatives:
                    if alt[1] == 'text/html':
                        queue.html_content = alt[0]


            if app:
                queue.app = app

            queue.save()

            if message.attachments:
                for attachment in message.attachments:
                    f = ContentFile(attachment[1])
                    f.name = attachment[0]
                    queue.attachment_set.create(
                        file_attachment=f
                    )

            num_sent += 1
        return num_sent

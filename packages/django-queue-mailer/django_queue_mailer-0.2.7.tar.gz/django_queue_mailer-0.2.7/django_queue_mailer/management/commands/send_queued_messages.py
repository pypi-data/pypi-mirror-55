import logging
from django.core.management.base import BaseCommand
from django_queue_mailer.models import Queue


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Can be run as a cronjob or directly to send queued messages.'

    def add_arguments(self, parser):
        parser.add_argument('--limit',
                            '-l',
                            action='store',
                            type=int,
                            dest='limit',
                            help='Limit the number of emails to process'
                            )

    def handle(self, *args, **options):
        if 'limit' in options:
            limit = options['limit']
        else:
            limit = None
        logger.debug('Limit={}'.format(limit))
        Queue.objects.send_queued(limit=limit)

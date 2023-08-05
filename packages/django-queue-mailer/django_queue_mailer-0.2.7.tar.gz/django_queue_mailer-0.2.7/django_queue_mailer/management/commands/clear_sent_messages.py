from django.core.management.base import BaseCommand
from django_queue_mailer.models import Queue


class Command(BaseCommand):
    help = 'Can be run as a cronjob or directly to clean out sent messages.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--offset',
            action='store',
            type=int,
            dest='offset',
            help='Only clear messages that are more than this many hours old'
        )

    def handle(self, *args, **options):
        MailerMessage.objects.clear_sent_messages(offset=options['offset'])

import os

VERSION = '0.2.7'


if 'DJANGO_SETTINGS_MODULE' in os.environ:
    from django.utils.translation import ugettext_lazy as _

    # custom language strings
    _('Django_Queue_Mailer')

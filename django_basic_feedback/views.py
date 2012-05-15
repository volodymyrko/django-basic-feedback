# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes

#Python imports
from datetime import datetime
import logging

#Django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site

#App imports
from models import Feedback
from forms import FeedbackForm

logger = logging.getLogger(__name__)

def add(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        
        if form.is_valid():
            if isinstance( request.user, User):
                form.instance.user = request.user
            if 'HTTP_REFERER' in request.META:
                form.instance.page = request.META['HTTP_REFERER']

            form.save()
            import pdb; pdb.set_trace()

            mail_from = getattr(settings, 'FEEDBACK_SEND_MAIL_FROM', False)
            mail_to = getattr(settings, 'FEEDBACK_SEND_MAIL_TO', False)
            if not mail_from and settings.ADMINS:
                mail_from = settings.ADMINS[0][1]
            if not mail_to and settings.ADMINS:
                mail_to = settings.ADMINS[0][1]
            if getattr(settings, 'FEEDBACK_SEND_MAIL', False) and mail_from and mail_to:
                site_name = Site.objects.get_current().name
                send_mail('Feedback from %s' % site_name, 'New Feedback message', mail_from,
                [mail_to], fail_silently=False)

            return HttpResponse('', mimetype="text/plain")
        else:
            logger.debug(form.errors)
            error_msg = []
            for field in form.errors:
                for error in form.errors[field]:
                    error_msg.append('%s: %s' % (form.fields[field].label, error))
            error_msg = '\n'.join(error_msg)
            
            return HttpResponseBadRequest(error_msg, mimetype="text/plain")
    else:
        return HttpResponseNotAllowed(["POST",])


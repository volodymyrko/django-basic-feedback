# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes

#Python imports
from datetime import datetime

#Django imports
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models


class Feedback(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	page = models.CharField(max_length="255", blank=True)
	text = models.TextField(validators=[MaxLengthValidator(255)])
	archived = models.BooleanField(default=False)


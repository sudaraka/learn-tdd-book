""" list models """

from django.db import models


class Item(models.Model):
    """ List item model """

    text = models.TextField()

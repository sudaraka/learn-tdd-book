""" list models """

from django.db import models


class List(models.Model):
    """ List model """

    pass


class Item(models.Model):
    """ List item model """

    text = models.TextField()
    list = models.ForeignKey(List)

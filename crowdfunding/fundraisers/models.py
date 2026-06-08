from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Fundraiser(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    data_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_fundraisers'
    )

class Pledge(models.Model):
    amount = models.IntegerField()
    # blank=True so donors can leave the comment empty
    comment = models.CharField(max_length=200, blank=True)
    anonymous = models.BooleanField()
    fundraiser = models.ForeignKey(
        'Fundraiser',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    # null/blank=True so people can donate WITHOUT being logged in (no supporter)
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges',
        null=True,
        blank=True
    )
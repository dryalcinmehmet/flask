from django.db import models
from django.contrib.auth.models import User


class Data(models.Model):
    text = models.TextField(max_length=255, blank=True)
    label = models.TextField(max_length=255, blank=True)


    def __str__(self):
        return "{} - {}".format(self.text, self.label)

    def save(self, *args, **kwargs):
        super(Data, self).save(*args, **kwargs)

    class Meta:
        db_table = 'dataset'



from django.db import models


class Legion(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_legion', 'View Legion'), )

    def __unicode__(self):
        return self.name

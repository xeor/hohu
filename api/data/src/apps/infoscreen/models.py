from django.db import models


class View(models.Model):
    enabled = models.BooleanField(default=False, db_index=True)

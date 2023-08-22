from django.db import models

class ScrapingParams(models.Model):
    param_name = models.CharField(max_length=100)
    param_value = models.CharField(max_length=100)

    def __str__(self):
        return self.param_name

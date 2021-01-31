from django.db import models

# Create your models here.
class BoardData(models.Model):
    title = models.CharField(max_length = 300)
    link = models.URLField()
    specific_id = models.CharField(max_length= 15)

    def __str__(self):
        return self.title


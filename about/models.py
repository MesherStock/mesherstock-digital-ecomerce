from django.db import models

# Create your models here.
class About(models.Model):
    about_image = models.ImageField(upload_to='media')
    content = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.content

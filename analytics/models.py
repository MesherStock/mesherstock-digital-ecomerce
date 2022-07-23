from django.conf import settings
from django.db import models


from tags.models import Tag
# Create your models here.
class TagViewManager(models.Manager):
  def add_count(self, user, tag):
    obj, create = self.model.objects.get_or_create(user=user, tag=tag)
    obj.count += 1
    obj.save()
    return obj



class TagView(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
  count = models.PositiveIntegerField(default=0)
  objects = TagViewManager()


  def __str__(self):
    return str(self.tag.title)

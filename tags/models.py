from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

# Create your models here.
from products.models import Product

class TagQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class TagManager(models.Manager):

    def get_queryset(self):
        return TagQueryset(self.model, using=self._db)

    def all(self, **kwargs):
        return super(TagManager, self).all(**kwargs).active()

class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    products = models.ManyToManyField(Product, blank=True)
    active = models.BooleanField(default=True)

    objects: TagManager()
    def __str__(self):
        return self.title


    def get_absolute_url(self):
        view_name = "tag:tag_detail"
        return reverse(view_name, kwargs={"slug": self.slug})


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance)
		
pre_save.connect(tag_pre_save_receiver, sender=Tag)

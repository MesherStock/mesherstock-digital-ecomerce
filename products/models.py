from django.urls import reverse
import datetime
from django.utils import timezone
from asyncio import protocols
from django.conf import settings
from django.db import models
from .storage import ProtectedStorage
User = settings.AUTH_USER_MODEL
from django.utils.text import slugify
from django.db.models.signals import pre_save
from sellers.models import Seller

from fileinput import filename
from PIL import ImageDraw, ImageFont, Image
from tkinter import SEL_FIRST, filedialog, Tk
import io

opacity_level = 170

# Create your models here.
# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'seller_{0}/{1}'.format(instance.seller, filename)
def download_media_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)


class Banner(models.Model):
    img = models.ImageField(blank=True, null=True)
    alt_text = models.CharField(max_length = 300)

    def __str__(self):
        return self.alt_text



class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=download_media_location, blank=True, null=True)
    media = models.FileField(upload_to=download_media_location, storage=ProtectedStorage, null=True, blank=True)
    video_link = models.TextField(blank=True)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    inventory = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    can_backorder = models.BooleanField(default=False)
    requires_shipping = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=True)
    image_size = models.CharField(max_length=20, null=True)
    location = models.CharField(max_length=150, null=True)
    recent_product = models.BooleanField(default=False)



    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        photo = Image.open(self.image.path)
        print("Image not saving")
        print(photo)
        if photo.mode in ("RGBA", "P"):
            photo = photo.convert("RGB")

        width, height = photo.size
        draw = ImageDraw.Draw(photo)
        myword = "MESHER"
        font_size = int(width / 15)
        try:
            font = ImageFont.truetype('I am Hueca.ttf', font_size)
        except:
            font = ImageFont.load_default(50)

        x, y = int(width/2), int(height/2)
        draw.text((x, y),myword, font=font, fill='#FFFF', stroke_width=5, stroke_fill="#222", anchor='ms')
        photo.save(self.image.path)



    def get_edit_url(self):
        view_name = "seller:update"
        return reverse(view_name, kwargs={"slug": self.slug})

    def get_edit_url(self):
        view_name = "seller:update_product"
        return reverse(view_name, kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return f"/product/{self.slug}/"



    def get_absolute_url(self):
        return reverse('product:detail', kwargs={"slug": self.slug})



    @property
    def order_btn_title(self):
        if self.can_order and not self.has_image():
            return "Backorder"
        if not self.can_order:
            return "can not purchase"
        return "Purchase"




    @property
    def can_order(self):
        if self.has_image():
            return True
        elif self.can_backorder:
            return True
        return False


    def has_image(self):
        if self.image:
            return True
        return False


    def has_inventory(self):
        return self.inventory > 0

    # def remove_item(self, count=1, save=True):
    #     current_inv = self.inventory
    #     current_inv -= count
    #     self.inventory = current_inv
    #     if save == True:
    #         self.save()
    #     return self.inventory

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Product.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
    
    
		
pre_save.connect(product_pre_save_receiver, sender=Product)



class Category(models.Model):
    # products = models.ManyToManyField(Product)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    class Meta: 
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-order"]

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse("product:category", args=[self.slug])






class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    image = models.ImageField(upload_to='products/image')
    title = models.CharField(max_length=120, null=True, blank=True)
    slug = models.SlugField()
    feautured_image = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.category)


    def get_absolute_url(self):
        return reverse("product:category_view")

    def get_url(self):
        return reverse("product:category_list", args={self.slug})


class FeaturedManager(models.Manager):
    def get_featured_instance(self):
        items = super(FeaturedManager, self).filter(date_start__lte=datetime.datetime.now(tz=timezone.utc)).filter(date_end__gte=datetime.datetime.now(tz=timezone.utc))
        all_items = super(FeaturedManager, self).all()
        if len(items) >= 1:
            return items[0]
        else:
            for i in all_items:
                if i.default:
                    return i
            return all_items[0]



class Featured(models.Model):
    title = models.CharField(max_length=150)
    products = models.ManyToManyField(Product,related_name='featured_product', limit_choices_to={'featured':True}, blank=True)
    date_start = models.DateField(auto_now=False, auto_now_add=False)
    date_end = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)


    objects = FeaturedManager()

    def __str__(self):
        return str(self.title)

    def get_featured(self):
        return self.products[:4]

    class Meta:
        verbose_name = "Featured"
        verbose_name_plural = "Featured"
from django.contrib import admin
from .models import Product, Category, CategoryImage, Featured, Banner
from django.utils.html import format_html
# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    def image_banner(self, obj):
        return format_html('<img src="{}" width="70" height="70" />'.format(obj.img.url))

    image_banner.short_description = 'Banner'
    list_display = ['image_banner', 'alt_text']

admin.site.register(Banner, BannerAdmin)

class productAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" width="70" height="70" />'.format(obj.image.url))

    image_tag.short_description = 'Image'
    list_display = ['image_tag','title','featured', 'is_digital', 'recent_product']
    list_editable = ['featured', 'is_digital', 'recent_product',]
    list_display_links = ['image_tag']


admin.site.register(Product, productAdmin)


class CategoryImageInline(admin.TabularInline):

    extra = 1
    model = CategoryImage
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CategoryImageInline,]
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)

admin.site.register(Featured)

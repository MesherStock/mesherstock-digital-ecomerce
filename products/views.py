from itertools import chain
from unicodedata import category
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from carts.models import CartItem
from .models import Category, CategoryImage, Product, Featured, Banner
from .forms import ProductForm
from emails.models import InventoryWaitList
from sellers.models import Seller
from sellers.mixins import SellerAccountMixin
from emails.forms import InventoryWaitListForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from tags.models import Tag
from .mixins import ProductManagerMixin
from Ecodig.mixins import MultiSlugMixin
# Create your views here.

def category_view(request):
    cat = Category.objects.all()

    category = CategoryImage.objects.filter(category__in=cat)
    context = {
        "category" : category,
        'cat':cat,
    }
    return render(request, 'products/category_list.html', context )

def category_list(request, slug):
    categories = Category.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        print(category)
        products = Product.objects.filter(category=category)
        print(products)

    context = {
        'category': category,
        'products': products,
        'categories': categories
    }
    return render(request, 'products/category.html', context)


class VendorListView(ListView):
    model = Product
    template_name = "products/product_list.html"



    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("vendor_name")
        seller = get_object_or_404(Seller, user__username=username)
        return seller


    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        context["vendor_name"] = str(self.get_object().user.username)
        return context

    def get_queryset(self, **kwargs):
        seller = self.get_object()
        qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
        # qs = qs.filter(is_featured=True)
        query = self.request.GET.get("q", "")
        if query:
            qs = qs.filter(Q(title__icontains=query)|Q(description__icontains=query))
        results = list(chain(qs))
        return results



def home_view(request):
    banner = Banner.objects.all()
    cat = Category.objects.all()
    recent_product = Product.objects.filter(recent_product=True).order_by('-recent_product')
    category = CategoryImage.objects.filter(category_id__in=cat)[:4]
    featured = Product.objects.filter(featured=True).order_by('-featured')[:7]
 
    context = {
        "category" : category,
        'cat':cat,
        'featured': featured,
        'banner': banner,
        'recent_product': recent_product,
    }
    return render(request, "index.html", context)



class ProductCreateView(SellerAccountMixin,CreateView):
    model = Product
    template_name = "products/create_view.html"
    form_class = ProductForm
    success_url = "/seller/dashboard"

    def form_valid(self, form):
        seller = self.get_account()
        form.instance.seller = seller
        valid_data = super(ProductCreateView, self).form_valid(form)
        # form.instance.managers.add(user)
        tags = form.cleaned_data.get("tags")
        category = form.cleaned_data.get("category")

        if tags:
            tag_list = tags.split(",")
            for tag in tag_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(form.instance)
        return valid_data






def featured_view(request, *args, **kwargs):
    qs = Product.objects.filter(featured=True).order_by('-id')
    product = None
    form = None
    can_order = False
    if qs.exists():
        product = qs.first()
    if product !=None:
        can_order = product.can_order
        if can_order:
            product_id = product.id
            request.session["product_id"]=product_id
        form = InventoryWaitListForm(request.POST or None, product=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            return redirect("/waitlist_success")

    context = {
        "object" : product,
        "form": form,
        "can_order": can_order,
    }
    return render(request, "products/detail.html", context)
    





def list_view(request, *args, **kwargs):
    products = Product.objects.all()

    context = {
        "products": products
    }
    return render(request, 'products/list.html', context)


def search_view(request, *args, **kwargs):
    try:
        q= request.GET.get("q", "")
    except:
        q = False
    product_queryset = Product.objects.filter(
        Q(title__icontains=q)|Q(content__icontains=q)|Q(category__title__icontains=q)
    ).order_by('id')
    results = list(chain(product_queryset))
    paginator = Paginator(results, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        "product_queryset": paged_products,
        "results":paged_products,
        "q": q
    }
    return render(request, 'products/search.html', context)


def product_detail_view(request,slug):
    qs = Product.objects.filter(slug=slug)
   
    product = None
    
    can_order = False
    form = None
    if qs.exists():
        product = qs.first()
    
    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(user=request.user, product=product).exists()
    else:
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    related = Product.objects.filter(category=product.category).exclude(slug=product.slug)
   


    if product != None:
        can_order = product.can_order
        if can_order:
            product_id = product.id
            request.session["product_id"]=product_id
        
        form = InventoryWaitListForm(request.POST or None, product=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            return redirect("/waitlist-success")

    context = {
        'object': product,
        "can_order": can_order,
        "form" : form,
        # "categories": categories,
        'related': related,
        'in_cart' : in_cart,
    }
    return render(request, "products/detail.html", context)



class ProductUpdateView(ProductManagerMixin,MultiSlugMixin,UpdateView):
    model = Product
    template_name = "forms.html"
    form_class = ProductForm


    def get_initial(self):
        initial = super(ProductUpdateView, self).get_initial()
        tag = self.get_object().tag_set.all()
        initial["tags"] =" ,".join([x.title for x in tag])
        return initial

    def form_valid(self, form):
        valid_data = super(ProductUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tag_list = tags.split(",")
            for tag in tag_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(self.get_object())
        return valid_data


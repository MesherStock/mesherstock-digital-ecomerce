from django.shortcuts import render

# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Tag
from analytics.models import TagView

class TagDetailView(DetailView):
    model = Tag
    template_name: str("tag/tag_detail.html")
    def get_context_data(self, **kwargs):
        context =super(TagDetailView, self).get_context_data(**kwargs)
        print(self.get_object().products.all())

        if self.request.user.is_authenticated:
            new_view = TagView.objects.add_count(self.request.user, tag=self.get_object())
            # analytic_obj,created = TagView.objects.get_or_create(user=self.request.user,tag=self.get_object())
            # analytic_obj.count += 1
            # analytic_obj.save()
        return context

class TagListView(ListView):
    model = Tag
    template_name = "tag/tag_list.html"

    def get_queryset(self, **kwargs):
        response = super(TagListView, self).get_queryset(**kwargs)
        response = Tag.objects.all().filter(active=True)
        return response
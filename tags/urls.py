from django.urls import path
from .views import (
    TagDetailView,
    TagListView
)

app_name = "tag"
urlpatterns = [
    path("<slug:slug>/", TagDetailView.as_view(), name="tag_detail"),
    path("", TagListView.as_view(), name="tag_list"),
]
from django.urls import path, re_path
from news.views import ComingSoonView, MainPageView, CreateView, ArticleView

urlpatterns = [
    path("", ComingSoonView.as_view()),
    path("news/", MainPageView.as_view()),
    path("news/create/", CreateView.as_view()),
    path("news/<int:link>/", ArticleView.as_view())
]

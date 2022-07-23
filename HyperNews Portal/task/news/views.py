import json
import datetime
import random

from django.http import Http404
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news")


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as file:
            articles = json.load(file)

            if "q" in request.GET:
                search_term = request.GET["q"]

                articles = list(filter(lambda x: search_term in x["title"], articles))

            dates = {}

            for article in articles:
                date = article["created"].split()[0]
                if date not in dates:
                    dates[date] = list()
                dates[date].append(article)

            dates = sorted(dates.items(), key=lambda x: x[0], reverse=True)

            if dates:
                return render(request, "news/news.html", context={"dates": dates})
            return render(request, "news/news.html", context={"dates": dates})


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create.html")

    def post(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as file:
            articles = json.load(file)
            text = request.POST["text"]
            title = request.POST["title"]
            created_time = datetime.datetime.now().strftime("%Y-%m-%d %X")
            used_links = list(map(lambda x: x["link"], articles))

            while True:
                link = random.randint(1, 1000000)
                if link not in used_links:
                    break

            articles.append({"created": created_time, "text": text, "title": title, "link": link})

        with open(settings.NEWS_JSON_PATH, "w") as file:
            file.write(json.dumps(articles))

        return redirect("/news")


class ArticleView(View):
    def get(self, request, link, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as file:
            articles = json.load(file)
            article = list(filter(lambda x: x["link"] == link, articles))
            if article:
                return render(request, "news/article.html", context={"article": article[0]})
            raise Http404()

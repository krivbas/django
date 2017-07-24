from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Article
from blog.serializers import ArticleSerializer

from utils import gen_page_list, build_url, send_email


def blogs(request):
    # data = {
    #     'first_name': 'John',
    #     'last_name': 'Smith'
    # }
    # return HttpResponse('qwjehgqwjkeh')
    # return HttpResponseRedirect('/qwertyui')
    # 'select * from blog_article' -> response -> django obj
    keyword = request.GET.get('keyword', '')
    page = request.GET.get('page', 1)
    p = Paginator(Article.objects.filter(title__contains=keyword).order_by('id'), 1)
    try:
        final_articles = p.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        final_articles = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        final_articles = p.page(p.num_pages)
    return render(request, 'blogs.html', {'articles': final_articles,
                                          'pagination': gen_page_list(page, p.num_pages),
                                          'keyword': keyword})


def single_blog(request, article_id):
    # try:
    #     # select * from blog_article where id = 2
    #     article = Article.objects.get(id=article_id)
    #     return render(request, 'single-blog.html', {'article': article})
    # except Article.DoesNotExist:
    #     raise Http404
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'single-blog.html', {'article': article})


def user_articles(request, user_id):
    # 13
    user = get_object_or_404(User, id=user_id)
    # user or 404
    articles = Article.objects.filter(author=user)
    return render(request, 'user-blog.html', {'articles': articles,
                                              'user': user})


def like_article(request, article_id):
    keyword = request.GET.get('keyword')
    page = request.GET.get('page')
    article = get_object_or_404(Article, id=article_id)
    if request.user in article.liked_by.all():
        article.liked_by.remove(request.user)
    else:
        article.liked_by.add(request.user)
    article.save()
    return HttpResponseRedirect(build_url('all_articles', get={'keyword': keyword, 'page': page}))


@api_view(['GET'])
def like_article_rest(request):
    content = {
        'first_name': 'John',
        'last_name': 'Smith'
    }
    send_email('hello', 'antonboksha@gmail.com', 'hello-mail.html', content)
    return Response({'success': True})


# class ArticlesView(ListAPIView):
#     queryset = Article.objects.all().order_by('id')
#     serializer_class = ArticleSerializer
#     pagination_class = PageNumberPagination


class ArticlesView(GenericAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            article = self.get_object(pk=kwargs.get('pk'))
            serializer = self.serializer_class(article)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
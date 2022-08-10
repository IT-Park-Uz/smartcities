from django.db.models import Q
from rest_framework import viewsets, status, permissions, pagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializer import (NewsSerializer, ArticleSerializer, QuestionSerializer, ImageQuestionSerializer,
                         TagsSerializer, ThemeSerializer, SearchNewsSerializer, SearchArticlesSerializer,
                         SearchQuestionsSerializer, NewsHistorySerializer, QuestionHistorySerializer,
                         ArticleHistorySerializer)
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme)
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

    def get_paginated_response(self, data):
        response = Response(data)
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        return response


class NewsApiView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def list(self, request, *args, **kwargs):
        news = self.queryset.filter(is_active=True, is_delete=False)
        serializer = NewsSerializer(news, many=True)
        for i in serializer.data:
            i['user'] = {'id': i['user']['id'], 'username': i['user']['username'],
                         'first_name': i['user']['first_name'], 'last_name': i['user']['last_name'],
                         'email': i['user']['email'], 'image': i['user']['image']}
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        new = self.queryset.filter(id=kwargs['pk'])
        if new:
            serializer = NewsSerializer(new, many=True)
            for i in serializer.data:
                i['user'] = {'id': i['user']['id'], 'username': i['user']['username'],
                             'first_name': i['user']['first_name'], 'last_name': i['user']['last_name'],
                             'email': i['user']['email'], 'image': i['user']['image']}
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        new = self.queryset.get(id=kwargs['pk'])
        new.is_active = False
        new.is_delete = True
        new.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchNewsView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = SearchNewsSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        # TODO: search fields: title, theme, tags
        news = News.objects.filter(Q(title__icontains=request.data['word']) | Q(theme__name__icontains=request.data['word']) | Q(tags__name=request.data['word']), is_active=True).order_by('view_count','created_at','like_count')
        articles = Article.objects.filter(Q(title__icontains=request.data['word']) | Q(theme__name__icontains=request.data['word']) | Q(tags__name=request.data['word']), is_active=True).order_by('view_count','created_at','like_count')
        questions = Question.objects.filter(Q(title__icontains=request.data['word']) | Q(theme__name__icontains=request.data['word']) | Q(tags__name=request.data['word']), is_active=True).order_by('view_count','created_at','like_count')
        nserializer = SearchNewsSerializer(news, many=True)
        aserializer = SearchArticlesSerializer(articles, many=True)
        qserializer = SearchQuestionsSerializer(questions, many=True)
        return Response({'news':nserializer.data,'articles':aserializer.data,'questions':qserializer.data}, status=status.HTTP_200_OK)

class UserNewsView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # TODO: History(active,passive) is_active = True, False beriladi
        news = self.get_queryset().filter(user=request.user, is_active=request.data['is_active'], is_delete=False)
        if news:
            serializer = NewsHistorySerializer(news, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleApiView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        articles = self.queryset.filter(is_active=True, is_delete=False)
        serializer = ArticleSerializer(articles, many=True)
        for i in serializer.data:
            i['user'] = {'id': i['user']['id'], 'username': i['user']['username'],
                         'first_name': i['user']['first_name'], 'last_name': i['user']['last_name'],
                         'email': i['user']['email'], 'image': i['user']['image']}
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        article = self.queryset.filter(id=kwargs['pk'])
        if article:
            serializer = ArticleSerializer(article, many=True)
            for i in serializer.data:
                i['user'] = {'id': i['user']['id'], 'username': i['user']['username'],
                             'first_name': i['user']['first_name'], 'last_name': i['user']['last_name'],
                             'email': i['user']['email'], 'image': i['user']['image']}
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        article = self.queryset.get(id=kwargs['pk'])
        article.is_active = False
        article.is_delete = True
        article.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        is_active = request.data  # TODO: History(active,passive) is_active True yoki False beriladi
        articles = self.get_queryset().filter(user=request.user, is_active=is_active['is_active'], is_delete=False)
        if articles:
            serializer = ArticleHistorySerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionApiView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        # questions = self.get_queryset()
        questions = self.queryset.filter(is_active=True, is_delete=False)
        serializer = QuestionSerializer(questions, many=True)
        for i in serializer.data:
            i['user'] = {'id': i['user']['id'], 'username': i['user']['username'],
                         'first_name': i['user']['first_name'], 'last_name': i['user']['last_name'],
                         'email': i['user']['email'], 'image': i['user']['image']}
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            question = self.queryset.get(id=kwargs['pk'])
            if question:
                serializer = QuestionSerializer(question, many=True)
                for i in serializer.data:
                    i['user'] = {'id': i['user']['id'], 'username': i['user']['username'],
                                 'first_name': i['user']['first_name'], 'last_name': i['user']['last_name'],
                                 'email': i['user']['email'], 'image': i['user']['image']}
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        question = self.queryset.get(id=kwargs['pk'])
        question.is_active = False
        question.is_delete = True
        question.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            question = Question.objects.create(user_id=1, type=data['type'], title=data['title'],
                                               description=data['description'])
            for i in data['tags']:
                tag = Tags.objects.get(id=int(i))
                question.tags.add(tag)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserQuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # TODO: History(active,passive) is_active True yoki False beriladi
        questions = self.get_queryset().filter(user=request.user, is_active=request.data['is_active'], is_delete=False)
        if questions:
            serializer = QuestionHistorySerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageQuestionApiView(viewsets.ModelViewSet):
    queryset = ImageQuestion.objects.all()
    serializer_class = ImageQuestionSerializer
    # permission_classes = [IsAuthenticated]


class TagsApiView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']


class ThemeApiView(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        if not request.data:
            themes = self.get_queryset().filter(parent=None)
            serializer = ThemeSerializer(themes, many=True)
            return Response(serializer.data)
        themes = self.get_queryset().filter(parent=int(request.data['tree_id']))
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)

from django.db.models import Q
from rest_framework import viewsets, status, permissions, pagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializer import (NewsSerializer, ArticleSerializer, QuestionSerializer, ImageQuestionSerializer,
                         TagsSerializer, ThemeSerializer, ReviewSerializer)
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme, Review)
from django.core.serializers import json


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
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        news = self.queryset.filter(is_active=True, is_delete=False)
        data = [{'id': new.id, 'theme': new.theme, 'title': new.title,
                 'images': new.imageURL,
                 'description': new.description, 'view_count': new.view_count,
                 'like_count': new.like_count,
                 'tags': [{'id': tag.id, 'name': tag.name} for tag in new.tags.all()],
                 'created_at': new.created_at.strftime('%d.%m.%Y %H:%M'),
                 'user': new.user.id} for new in news]
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        new = self.queryset.get(id=kwargs['pk'])
        if new:
            data = [{'id': new.id, 'theme': new.theme, 'title': new.title, 'image': new.imageURL,
                     'description': new.description, 'view_count': new.view_count,
                     'like_count': new.like_count,
                     'tags': [{'id': tag.id, 'name': tag.name} for tag in new.tags.all()],
                     'created_at': new.created_at.strftime('%d.%m.%Y %H:%M'),
                     'user': new.user.id,
                     'is_active': new.is_active}]
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        new = self.queryset.get(id=kwargs['pk'])
        new.is_active = False
        new.is_delete = True
        new.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserNewsView(ListAPIView):
    queryset = News.objects.all()
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        is_active = request.data  # TODO: History(active,passive) is_active True yoki False beriladi
        news = self.get_queryset().filter(user=request.user, is_active=is_active['is_active'], is_delete=False)
        if news:
            for new in news:
                data = [{'id': new.id, 'title': new.title,
                         'images': [q.imageURL for q in ImageQuestion.objects.filter(question=new)],
                         'tags': [{'id': tag.id, 'name': tag.name} for tag in new.tags.all()],
                         'created_at': new.created_at.strftime('%d.%m.%Y %H:%M'),
                         'user': new.user.id}]
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleApiView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        articles = self.queryset.filter(is_active=True, is_delete=False)
        data = [{'id': article.id, 'theme': article.theme, 'title': article.title, 'images': article.imageURL,
                 'description': article.description, 'view_count': article.view_count,
                 'like_count': article.like_count,
                 'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags.all()],
                 'created_at': article.created_at.strftime('%d.%m.%Y %H:%M'),
                 'user': article.user.id} for article in articles]
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        article = self.queryset.get(id=kwargs['pk'])
        if article:
            data = [{'id': article.id, 'theme': article.theme, 'title': article.title, 'image': article.imageURL,
                     'description': article.description, 'view_count': article.view_count,
                     'like_count': article.like_count,
                     'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags.all()],
                     'created_at': article.created_at.strftime('%d.%m.%Y %H:%M'),
                     'user': article.user.id}]
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        article = self.queryset.get(id=kwargs['pk'])
        article.is_active = False
        article.is_delete = True
        article.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserArticleView(ListAPIView):
    queryset = Article.objects.all()
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        is_active = request.data  # TODO: History(active,passive) is_active True yoki False beriladi
        articles = self.get_queryset().filter(user=request.user, is_active=is_active['is_active'], is_delete=False)
        if articles:
            for article in articles:
                data = [{'id': article.id, 'title': article.title,
                         'images': [q.imageURL for q in ImageQuestion.objects.filter(question=article)],
                         'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags.all()],
                         'created_at': article.created_at.strftime('%d.%m.%Y %H:%M'),
                         'user': article.user.id}]

            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionApiView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        questions = self.get_queryset()
        # questions = self.queryset.filter(is_active=True, is_delete=False)
        data = [{'id': question.id, 'theme': question.theme, 'type': question.type, 'title': question.title,
                 'images': [q.imageURL for q in ImageQuestion.objects.filter(question=question)],
                 'description': question.description, 'view_count': question.view_count,
                 'like_count': question.like_count,
                 'tags': [{'id': tag.id, 'name': tag.name} for tag in question.tags.all()],
                 'created_at': question.created_at.strftime('%d.%m.%Y %H:%M'),
                 'user': question.user.id} for question in questions]
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            question = self.queryset.get(id=kwargs['pk'])
            if question:
                data = [{'id': question.id, 'theme': question.theme, 'type': question.type, 'title': question.title,
                         'images': [q.imageURL for q in ImageQuestion.objects.filter(question=question)],
                         'description': question.description, 'view_count': question.view_count,
                         'like_count': question.like_count,
                         'tags': [{'id': tag.id, 'name': tag.name} for tag in question.tags.all()],
                         'created_at': question.created_at.strftime('%d.%m.%Y %H:%M'),
                         'user': question.user.id}]
                return Response(data, status=status.HTTP_200_OK)
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
            datas = [{'id': question.id, 'theme': question.theme, 'type': question.type, 'title': question.title,
                      'images': [q.imageURL for q in ImageQuestion.objects.filter(question=question)],
                      'description': question.description, 'view_count': question.view_count,
                      'like_count': question.like_count,
                      'tags': [{'id': tag.id, 'name': tag.name} for tag in question.tags.all()],
                      'created_at': question.created_at.strftime('%d.%m.%Y %H:%M'),
                      'user': question.user.id}]
            return Response(datas, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserQuestionView(ListAPIView):
    queryset = Question.objects.all()
    http_method_names = ['get']
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        is_active = request.data  # TODO: History(active,passive) is_active True yoki False beriladi
        questions = self.get_queryset().filter(user=request.user, is_active=is_active['is_active'], is_delete=False)
        if questions:
            for question in questions:
                data = [{'id': question.id, 'title': question.title,
                         'images': [q.imageURL for q in ImageQuestion.objects.filter(question=question)],
                         'tags': [{'id': tag.id, 'name': tag.name} for tag in question.tags.all()],
                         'created_at': question.created_at.strftime('%d.%m.%Y %H:%M'),
                         'user': question.user.id}]

            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageQuestionApiView(viewsets.ModelViewSet):
    queryset = ImageQuestion.objects.all()
    serializer_class = ImageQuestionSerializer
    # permission_classes = [IsAuthenticated]


class TagsApiView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    # permission_classes = [IsAuthenticated]
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



class ReviewApiView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

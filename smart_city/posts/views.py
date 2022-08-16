from django.db.models import Q
from rest_framework import viewsets, status, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializer import (NewsSerializer, ArticleSerializer, QuestionSerializer, ImageQuestionSerializer,
                         TagsSerializer, ThemeSerializer, SearchNewsSerializer, SearchArticlesSerializer,
                         SearchQuestionsSerializer, NewsHistorySerializer, QuestionHistorySerializer,
                         ArticleHistorySerializer, NewsReviewSerializer, ArticleReviewSerializer,
                         QuestionReviewSerializer)
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme, NewsReview, ArticleReview,
                                     QuestionReview)
from django.contrib.auth import get_user_model

User = get_user_model()


class NewsApiView(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True, is_delete=False)
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        try:
            new = self.queryset.get(id=int(kwargs['pk']))
            if new:
                serializer = NewsSerializer(new, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        new = self.queryset.get(id=kwargs['pk'])
        new.is_active = False
        new.is_delete = True
        new.save()
        return Response(status=status.HTTP_200_OK)


class SearchNewsView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = SearchNewsSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        # TODO: search fields: title, theme, tags
        try:
            news = News.objects.filter(
                Q(title__icontains=request.query_params['word']) | Q(
                    theme__name__icontains=request.query_params['word']) | Q(
                    tags__name=request.query_params['word']), is_active=True).order_by('view_count', 'created_at',
                                                                                       'like_count')
            serializer = SearchNewsSerializer(news, many=True)
            return Response({'news': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': status.HTTP_204_NO_CONTENT})


class SearchArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = SearchArticlesSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        # TODO: search fields: title, theme, tags
        try:
            articles = Article.objects.filter(
                Q(title__icontains=request.query_params['word']) | Q(
                    theme__name__icontains=request.query_params['word']) | Q(
                    tags__name=request.query_params['word']), is_active=True).order_by('view_count', 'created_at',
                                                                                       'like_count')
            serializer = SearchArticlesSerializer(articles, many=True)
            return Response({'articles': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': status.HTTP_204_NO_CONTENT})


class SearchQuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = SearchQuestionsSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        # TODO: search fields: title, theme, tags
        try:
            questions = Question.objects.filter(
                Q(title__icontains=request.query_params['word']) | Q(
                    theme__name__icontains=request.query_params['word']) | Q(
                    tags__name=request.query_params['word']), is_active=True).order_by('view_count', 'created_at',
                                                                                       'like_count')
            serializer = SearchQuestionsSerializer(questions, many=True)
            return Response({'question': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': status.HTTP_204_NO_CONTENT})


class UserNewsView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # TODO: History(active,passive) is_active = True, False beriladi
        try:
            news = self.get_queryset().filter(user=request.user, is_active=request.query_params['active'],
                                              is_delete=False).order_by('created_at')
        except:
            return Response({"status": "Not fount active key"}, status=status.HTTP_400_BAD_REQUEST)
        if news:
            serializer = NewsHistorySerializer(news, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleApiView(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True, is_delete=False)
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        try:
            article = self.queryset.get(id=int(kwargs['pk']))
            if article:
                serializer = ArticleSerializer(article, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        article = self.queryset.get(id=kwargs['pk'])
        article.is_active = False
        article.is_delete = True
        article.save()
        return Response(status=status.HTTP_200_OK)


class UserArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # TODO: History(active,passive) is_active True yoki False beriladi
        try:
            articles = self.get_queryset().filter(user=request.user, is_active=request.query_params['active'],
                                                  is_delete=False).order_by('created_at')
        except:
            return Response({"status": "Not fount active key"}, status=status.HTTP_400_BAD_REQUEST)
        if articles:
            serializer = ArticleHistorySerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionApiView(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True, is_delete=False)
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        try:
            question = self.queryset.get(id=int(kwargs['pk']))
            if question:
                serializer = QuestionSerializer(question, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        question = self.queryset.get(id=kwargs['pk'])
        question.is_active = False
        question.is_delete = True
        question.save()
        return Response(status=status.HTTP_200_OK)


class UserQuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # TODO: History(active,passive) is_active True yoki False beriladi
        try:
            questions = self.get_queryset().filter(user=request.user, is_active=request.query_params['active'],
                                                   is_delete=False).order_by('created_at')
        except:
            return Response({"status": "Not fount active key"}, status=status.HTTP_400_BAD_REQUEST)
        if questions:
            serializer = QuestionHistorySerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageQuestionApiView(viewsets.ModelViewSet):
    queryset = ImageQuestion.objects.all()
    serializer_class = ImageQuestionSerializer
    permission_classes = [IsAuthenticated]


class TagsApiView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']


class ThemeApiView(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.query_params:
            themes = self.get_queryset().filter(parent=None)
            serializer = ThemeSerializer(themes, many=True)
            return Response(serializer.data)
        themes = self.get_queryset().filter(parent=int(request.query_params['tree_id']))
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)


class NewsReviewView(viewsets.ModelViewSet):
    queryset = NewsReview.objects.all().order_by('-created_at')
    serializer_class = NewsReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        if not request.query_params:
            return Response({'message': "You should give id in params"}, status=status.HTTP_204_NO_CONTENT)
        new_id = request.query_params['id']
        # TODO: ichki comment bilan ishlash
        comments = self.get_queryset().filter(news__pk=new_id, parent=None)
        serializer = NewsReviewSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleReviewView(viewsets.ModelViewSet):
    queryset = ArticleReview.objects.all()
    serializer_class = ArticleReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']


class QuestionReviewView(viewsets.ModelViewSet):
    queryset = QuestionReview.objects.all()
    serializer_class = QuestionReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

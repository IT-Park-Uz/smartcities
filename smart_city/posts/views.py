from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializer import (NewsSerializer, ArticleSerializer, QuestionSerializer, ImageQuestionSerializer,
                         TagsSerializer, ThemeSerializer, SearchNewsSerializer, SearchArticlesSerializer,
                         SearchQuestionsSerializer, NewsReviewSerializer, ArticleReviewSerializer,
                         QuestionReviewSerializer, NewsWriteSerializer, ArticleWriteSerializer,
                         QuestionWriteSerializer)
from .mixin import ReadWriteSerializerMixin
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme, NewsReview, ArticleReview,
                                     QuestionReview)
from django.contrib.auth import get_user_model

from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

User = get_user_model()


class NewsApiView(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True).annotate(comment_count=Count("newsreview")).order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    read_serializer_class = NewsSerializer
    write_serializer_class = NewsWriteSerializer

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))
        try:
            new = queryset.filter(id=int(kwargs['pk'])).first()
            new.view_count += 1
            new.save()
            if new:
                serializer = NewsSerializer(new, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        new = self.queryset.filter(id=kwargs['pk']).first()
        if new:
            new.is_active = False
            new.is_delete = True
            new.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_like(self, request, *args, **kwargs):
        obj = News.objects.filter(id=int(kwargs['pk'])).first()
        if obj.user_liked.filter(id=request.user.id).exists():
            obj.user_liked.remove(request.user)
        else:
            obj.user_liked.add(request.user)
        return Response(status=status.HTTP_200_OK)

    # @action(detail=False, methods=['patch'], url_name='top_like')
    # def top_like(self, request, *args, **kwargs):
    #     news = self.get_queryset().order_by('user_liked')
    #     if news:
    #         serializer = NewsSerializer(news, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='key',
                         description="key is required in params")
    ],
        description="THE URL USES FOR SEARCHING NEWS ")
)
class SearchNewsView(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True)
    serializer_class = SearchNewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        try:
            key = request.query_params['key']
            news = self.get_queryset().filter(
                Q(title__icontains=key) | Q(
                    theme__name__icontains=key) | Q(
                    tags__name=key)).order_by('view_count')
            if news:
                page = self.paginate_queryset(news)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                serializer = self.get_serializer(news, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='key',
                         description="key is required in params")
    ],
        description="THE URL USES FOR SEARCHING ARTICLES ")
)
class SearchArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True)
    serializer_class = SearchArticlesSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        try:
            articles = self.queryset.filter(
                Q(title__icontains=request.query_params['key']) | Q(
                    theme__name__icontains=request.query_params['key']) | Q(
                    tags__name=request.query_params['key'])).order_by('view_count', 'created_at')
            page = self.paginate_queryset(articles)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='key',
                         description="key is required in params")
    ],
        description="THE URL USES FOR SEARCHING QUESTIONS ")
)
class SearchQuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = SearchQuestionsSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        try:
            questions = self.get_queryset().filter(
                Q(title__icontains=request.query_params['key']) | Q(
                    theme__name__icontains=request.query_params['key']) | Q(
                    tags__name=request.query_params['key'])).order_by('view_count', 'created_at')
            page = self.paginate_queryset(questions)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='status',
                         description="status is required in params")
    ],
        description="STATUS USES FOR TO GET NEWS OF USER, YOU SHOULD GIVE TRUE OR FALSE IN STATUS")
)
class UserNewsView(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_delete=False).annotate(comment_count=Count("newsreview")).order_by('-created_at')
    permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            stat = request.query_params['status']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user, is_active=stat).annotate(
            is_liked=Exists(self.get_queryset().filter(user_liked__id=request.user.id, id=OuterRef('pk')))))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleApiView(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True).annotate(comment_count=Count("articlereview")).order_by(
        '-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    read_serializer_class = ArticleSerializer
    write_serializer_class = ArticleWriteSerializer

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))
        try:
            article = queryset.filter(id=int(kwargs['pk'])).first()
            article.view_count += 1
            article.save()
            if article:
                serializer = ArticleSerializer(article, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        article = self.get_queryset().filter(id=kwargs['pk']).first()
        if article:
            article.is_active = False
            article.is_delete = True
            article.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_like(self, request, *args, **kwargs):
        obj = Article.objects.filter(id=int(kwargs['pk'])).first()
        if obj.user_liked.filter(id=request.user.id).exists():
            obj.user_liked.remove(request.user)
        else:
            obj.user_liked.add(request.user)
        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='status',
                         description="status is required in params")
    ],
        description="STATUS USES FOR TO GET ARTICLES OF USER, YOU SHOULD GIVE TRUE OR FALSE IN STATUS")
)
class UserArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_delete=False).annotate(comment_count=Count("articlereview")).order_by(
        '-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            stat = request.query_params['status']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(
            self.get_queryset().filter(user=request.user, is_active=stat).annotate(
                is_liked=Exists(self.get_queryset().filter(
                    user_liked__id=request.user.id,
                    id=OuterRef('pk')
                ))))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionApiView(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True).annotate(comment_count=Count("questionreview")).order_by(
        '-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    read_serializer_class = QuestionSerializer
    write_serializer_class = QuestionWriteSerializer

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))
        try:
            question = queryset.filter(id=int(kwargs['pk'])).first()
            question.view_count += 1
            question.save()
            if question:
                serializer = QuestionSerializer(question, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        question = self.get_queryset().filter(id=kwargs['pk']).first()
        if question:
            question.is_active = False
            question.is_delete = True
            question.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_like(self, request, *args, **kwargs):
        obj = Question.objects.filter(id=int(kwargs['pk'])).first()
        if obj.user_liked.filter(id=request.user.id).exists():
            obj.user_liked.remove(request.user)
        else:
            obj.user_liked.add(request.user)
        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='status',
                         description="status is required in params")
    ],
        description="STATUS USES FOR TO GET QUESTIONS OF USER, YOU SHOULD GIVE TRUE OR FALSE IN STATUS")
)
class UserQuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_delete=False).annotate(comment_count=Count("questionreview")).order_by(
        '-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            stat = request.query_params['status']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(
            self.get_queryset().filter(user=request.user, is_active=stat).annotate(
                is_liked=Exists(self.get_queryset().filter(
                    user_liked__id=request.user.id,
                    id=OuterRef('pk')
                ))))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageQuestionApiView(viewsets.ModelViewSet):
    queryset = ImageQuestion.objects.all()
    serializer_class = ImageQuestionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='status',
                         description="status is required in params")
    ],
        description="STATUS USES FOR TO GET NEWS OF USER, YOU SHOULD GIVE TRUE OR FALSE IN STATUS")
)
class TagsApiView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        # TODO: search fields: tag
        try:
            tag = self.get_queryset().filter(name__icontains=request.query_params['tag'])
            serializer = TagsSerializer(tag, many=True)
            return Response({'tag': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': status.HTTP_204_NO_CONTENT})


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='tree_id',
                         description="tree_id is required in params")
    ],
        description="TREE_ID USES FOR TO GET THEMES, YOU SHOULD GIVE IT AS A INTEGER")
)
class ThemeApiView(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        if not request.query_params:
            themes = self.get_queryset().filter(parent=None)
            serializer = ThemeSerializer(themes, many=True)
            return Response(serializer.data)
        try:
            themes = self.get_queryset().filter(parent=int(request.query_params['tree_id']))
        except:
            return Response({'error': 'tree_id didn\'t match in params'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='tree_id',
                         description="tree_id is required in params")
    ],
        description="TREE_ID IS REQUIRED FOR TO GET NEWS, YOU SHOULD GIVE IT AS A INTEGER AND GET NEWS")
)
class ThemeGroupNewsView(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True).annotate(comment_count=Count("newsreview")).order_by(
        '-created_at')
    serializer_class = NewsSerializer
    http_method_names = ['get']

    def get_serializer_class(self):
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            id = int(request.query_params.get('theme_id'))
        except:
            return Response({'message': 'theme_id not fount in params'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        news = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk'))))).filter(theme_id=id)
        page = self.paginate_queryset(news)
        if page is not None:
            serializer = NewsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='tree_id',
                         description="tree_id is required in params")
    ],
        description="TREE_ID IS REQUIRED FOR TO GET QUESTIONS, YOU SHOULD GIVE IT AS A INTEGER AND GET QUESTIONS")
)
class ThemeGroupQuestionsView(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True).annotate(comment_count=Count("questionreview")).order_by(
        '-created_at')
    serializer_class = QuestionSerializer
    http_method_names = ['get']

    def get_serializer_class(self):
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            id = int(request.query_params.get('theme_id'))
        except:
            return Response({'message': 'theme_id not fount in params'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        questions = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk'))))).filter(theme_id=id)
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = QuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='tree_id',
                         description="tree_id is required in params")
    ],
        description="TREE_ID IS REQUIRED FOR TO GET ARTICLES, YOU SHOULD GIVE IT AS A INTEGER AND GET ARTICLES")
)
class ThemeGroupArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True).annotate(comment_count=Count("articlereview")).order_by(
        '-created_at')
    serializer_class = ArticleSerializer
    http_method_names = ['get']

    def get_serializer_class(self):
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            id = int(request.query_params.get('theme_id'))
        except:
            return Response({'message': 'theme_id not fount in params'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        articles = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk'))))).filter(theme_id=id)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='id',
                         description="id is required in params")
    ],
        description="ID IS REQUIRED FOR TO GET A NEWS'S COMMENTS , YOU SHOULD GIVE IT AS A INTEGER ALSO CAN POST A COMMENT")
)
class NewsReviewView(viewsets.ModelViewSet):
    serializer_class = NewsReviewSerializer  # noqa F405
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = NewsReview.objects.all().order_by('-created_at')
        try:
            news_id = self.request.query_params['id']
        except:
            return []
        if news_id is not None:
            queryset = queryset.filter(news__pk=news_id)
        return queryset


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='id',
                         description="id is required in params")
    ],
        description="ID IS REQUIRED FOR TO GET A ARTICLE'S COMMENTS , YOU SHOULD GIVE IT AS A INTEGER ALSO CAN POST A COMMENT")
)
class ArticleReviewView(viewsets.ModelViewSet):
    serializer_class = ArticleReviewSerializer  # noqa F405
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = ArticleReview.objects.all().order_by('-created_at')
        try:
            article_id = self.request.query_params['id']
        except:
            return []
        if article_id is not None:
            queryset = queryset.filter(article__pk=article_id)
        return queryset


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='id',
                         description="id is required in params")
    ],
        description="ID IS REQUIRED FOR TO GET A QUESTION'S COMMENTS , YOU SHOULD GIVE IT AS A INTEGER ALSO CAN POST A COMMENT")
)
class QuestionReviewView(viewsets.ModelViewSet):
    serializer_class = QuestionReviewSerializer  # noqa F405
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = QuestionReview.objects.all().order_by('-created_at')
        try:
            question_id = self.request.query_params['id']
        except:
            return []
        if question_id is not None:
            queryset = queryset.filter(question__pk=question_id)
        return queryset


class LikeNewsView(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True).annotate(comment_count=Count("newsreview"))
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))

        page = self.paginate_queryset(queryset.order_by('user_liked'))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset.order_by('user_liked'), many=True)
        return Response(serializer.data)


class ReadNewsView(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True).order_by("-view_count").annotate(comment_count=Count("newsreview"))
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LikeArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True).annotate(comment_count=Count("articlereview"))
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))

        page = self.paginate_queryset(queryset.order_by('user_liked'))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset.order_by('user_liked'), many=True)
        return Response(serializer.data)


class ReadArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True).order_by("-view_count").annotate(
        comment_count=Count("articlereview"))
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LikeQuestionsView(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True).annotate(comment_count=Count("questionreview"))
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))

        page = self.paginate_queryset(queryset.order_by('user_liked'))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset.order_by('user_liked'), many=True)
        return Response(serializer.data)


class ReadQuestionsView(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True).order_by('-view_count').annotate(
        comment_count=Count("questionreview"))
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", 'theme', 'tags')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().annotate(is_liked=Exists(self.get_queryset().filter(
            user_liked__id=request.user.id,
            id=OuterRef('pk')
        ))))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

from rest_framework import serializers
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme)
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','image', 'username','email','organization_name','work_name','bio',]

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title','image','created_at','theme', 'description','tags','view_count','like_count','user']
        depth = 1


class NewsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title','image','created_at','theme', 'description','tags','view_count','like_count']
        depth = 1

class SearchNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title','theme','tags','description']
        depth = 1

class SearchArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title','theme','tags','description']
        depth = 1

class SearchQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title','theme','tags','description']
        depth = 1


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title','image','created_at','theme', 'description','tags','view_count','like_count','user']
        depth = 1


class ArticleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title','image','created_at','theme', 'description','tags','view_count','like_count']
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'created_at', 'theme', 'description', 'tags', 'view_count', 'like_count','user']
        depth = 1


class QuestionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'created_at', 'theme', 'description', 'tags', 'view_count', 'like_count']
        depth = 1


class ImageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageQuestion
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'
        depth = 1

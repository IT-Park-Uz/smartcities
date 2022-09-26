from rest_framework import serializers
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme, NewsReview, ArticleReview,
                                     QuestionReview, Notification)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'username', 'email', 'organization_name', 'work_name',
                  'bio']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        exclude = ['is_active']


class NewsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = News
        exclude = ['user_liked', 'is_delete', 'is_active', 'is_draft', 'saved_collections']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "NEWS"
        return response


class NewsWriteSerializer(serializers.ModelSerializer):
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tags.objects.all()
    )

    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        news = News.objects.create(**validated_data)
        if tag:
            for i in tag:
                news.tags.add(i)
        return news


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Article
        exclude = ['user_liked', 'is_delete', 'is_active', 'is_draft', 'saved_collections']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "ARTICLE"
        return response


class ArticleWriteSerializer(serializers.ModelSerializer):
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tags.objects.all()
    )

    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        article = Article.objects.create(**validated_data)
        if tag:
            for i in tag:
                article.tags.add(i)
        return article


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Question
        exclude = ['user_liked', 'is_delete', 'is_active', 'is_draft', 'saved_collections']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "QUESTION"
        return response


class QuestionWriteSerializer(serializers.ModelSerializer):
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tags.objects.all()
    )

    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        question = Question.objects.create(**validated_data)
        if tag:
            for i in tag:
                question.tags.add(i)
        return question


class ImageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageQuestion
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class NewsReviewSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = NewsReview
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response


class ArticleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleReview
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response


class QuestionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionReview
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response


class UserSavedCollectionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField(max_length=10)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ['is_active', 'user_read']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['is_read'] = instance.is_read
        return response

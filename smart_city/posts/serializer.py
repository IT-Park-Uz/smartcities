from rest_framework import serializers
from smart_city.posts.models import (News, Article, Question, Tags, Theme, NewsReview, ArticleReview,
                                     QuestionReview, Notification, UserUploadImage)
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'username', 'email', 'organization_name', 'work_name',
                  'bio', 'country_code']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'username', 'country_code']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        exclude = ['is_active']


class NewsPartSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.IntegerField(read_only=True)
    saved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = News
        exclude = ['user_liked', 'is_delete', 'is_draft', 'saved_collections', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "NEWS"
        return response


class NewsSideBarSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = News
        fields = ["id", "title", "like_count", "view_count"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['description'] = None
        response['type'] = "NEWS"
        return response


class NewsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.IntegerField(read_only=True)
    saved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = News
        exclude = ['user_liked', 'is_delete', 'is_draft', 'saved_collections']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "NEWS"
        return response


class NewsWriteSerializer(serializers.ModelSerializer):
    tags_ids = serializers.CharField(max_length=50, allow_null=True)

    class Meta:
        model = News
        exclude = ['user_liked', 'is_delete', 'is_active', 'is_draft', 'saved_collections', 'tags']

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        news = News.objects.create(**validated_data)
        if tag:
            for i in tag.split(","):
                t = Tags.objects.get(id=int(i))
                news.tags.add(t)
        return news


class ArticlePartSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.IntegerField(read_only=True)
    saved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        exclude = ['user_liked', 'is_delete', 'is_draft', 'saved_collections', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "ARTICLE"
        return response


class ArticleSideBarSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "like_count", "view_count"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['description'] = None
        response['type'] = "ARTICLE"
        response['like_count'] = instance.like_count
        return response


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.IntegerField(read_only=True)
    saved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        exclude = ['user_liked', 'is_delete', 'is_draft', 'saved_collections']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "ARTICLE"
        return response


class ArticleWriteSerializer(serializers.ModelSerializer):
    tags_ids = serializers.CharField(max_length=50, allow_null=True)

    class Meta:
        model = Article
        exclude = ['user_liked', 'is_delete', 'is_active', 'is_draft', 'saved_collections', 'tags']

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        article = Article.objects.create(**validated_data)
        if tag:
            for i in tag.split(","):
                t = Tags.objects.get(id=int(i))
                article.tags.add(t)
        return article


class QuestionPartSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.IntegerField(read_only=True)
    saved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        exclude = ['user_liked', 'is_delete', 'is_draft', 'saved_collections', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['like_count'] = instance.like_count
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "QUESTION"
        return response


class QuestionSideBarSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "title", "like_count", "view_count"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['description'] = None
        response['type'] = "QUESTION"
        return response


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    like_count = serializers.IntegerField(read_only=True)
    saved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        exclude = ['user_liked', 'is_delete', 'is_draft', 'saved_collections']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['is_saved'] = instance.is_saved
        response['type'] = "QUESTION"
        return response


class QuestionWriteSerializer(serializers.ModelSerializer):
    tags_ids = serializers.CharField(max_length=50, allow_null=True)

    class Meta:
        model = Question
        exclude = ['user_liked', 'is_delete', 'is_active', 'is_draft', 'saved_collections', 'tags']

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        question = Question.objects.create(**validated_data)
        if tag:
            for i in tag.split(","):
                t = Tags.objects.get(id=int(i))
                question.tags.add(t)
        return question


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
        response['user'] = UserDataSerializer(instance.user).data
        return response


class ArticleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleReview
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
        return response


class QuestionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionReview
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserDataSerializer(instance.user).data
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


class UserUploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUploadImage
        fields = '__all__'


class UserAccountNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = "NEWS"
        return response


class UserAccountArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = "ARTICLE"
        return response


class UserAccountQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = "QUESTION"
        return response

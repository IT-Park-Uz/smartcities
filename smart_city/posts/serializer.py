from rest_framework import serializers
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme, NewsReview, ArticleReview,
                                     QuestionReview)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'username', 'email', 'organization_name', 'work_name',
                  'bio', ]


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.first_name')
    tags = TagsSerializer(read_only=True, many=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tags.objects.all()
    )

    class Meta:
        model = News
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['comments_count'] = self.get_comments(instance)
        return response

    def get_comments(self, obj):
        posts = obj.newsreview_set.all().count()
        return posts

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        new = News.objects.create(**validated_data)
        if tag:
            for i in tag:
                new.tags.add(i)
        return new


class NewsHistorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'created_at', 'theme', 'description', 'tags', 'view_count', 'like_count']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        return response


class SearchNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'theme', 'tags', 'description']
        depth = 1


class SearchArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'theme', 'tags', 'description']
        depth = 1


class SearchQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'theme', 'tags', 'description']
        depth = 1


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tags.objects.all()
    )

    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['comments_count'] = self.get_comments(instance)
        return response

    def get_comments(self, obj):
        posts = obj.articlereview_set.all().count()
        return posts

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        article = Article.objects.create(**validated_data)
        if tag:
            for i in tag:
                article.tags.add(i)
        return article


class ArticleHistorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'created_at', 'theme', 'description', 'tags', 'view_count', 'like_count']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        return response


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tags.objects.all()
    )

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['comments_count'] = self.get_comments(instance)
        return response

    def get_comments(self, obj):
        posts = obj.questionreview_set.all().count()
        return posts

    def create(self, validated_data):
        tag = validated_data.pop("tags_ids", None)
        validated_data["user"] = self.context["request"].user
        question = Question.objects.create(**validated_data)
        if tag:
            for i in tag:
                question.tags.add(i)
        return question


class QuestionHistorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'created_at', 'theme', 'description', 'tags', 'view_count', 'like_count']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        return response


class ImageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageQuestion
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name', 'tree_id', 'parent', ]
        depth = 1


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

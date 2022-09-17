from rest_framework import serializers
from smart_city.posts.models import (News, Article, Question, ImageQuestion, Tags, Theme, NewsReview, ArticleReview,
                                     QuestionReview, UserLikedNews, UserLikedArticles, UserLikedQuestions)
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
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['like_count'] = instance.like_count
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


class NewsHistorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'created_at', 'theme', 'description', 'tags', 'view_count']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        response['comments_count'] = instance.comment_count
        response['like_count'] = instance.like_count
        return response


class SearchNewsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'theme', 'tags', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        return response



class SearchArticlesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'theme', 'tags', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        return response


class SearchQuestionsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'theme', 'tags', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        return response


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['like_count'] = instance.like_count
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


class ArticleHistorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'created_at', 'theme', 'description', 'tags', 'view_count']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        response['comments_count'] = instance.comment_count
        response['like_count'] = instance.like_count
        return response


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['theme'] = ThemeSerializer(instance.theme).data
        response['is_liked'] = instance.is_liked
        response['comments_count'] = instance.comment_count
        response['like_count'] = instance.like_count
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


class QuestionHistorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'created_at', 'theme', 'description', 'tags', 'view_count']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['theme'] = ThemeSerializer(instance.theme).data
        response['comments_count'] = instance.comment_count
        response['like_count'] = instance.like_count
        return response


class ImageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageQuestion
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name']


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


class UserLikedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLikedNews
        fields = '__all__'


class UserLikedArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLikedArticles
        fields = '__all__'


class UserLikedQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLikedQuestions
        fields = '__all__'

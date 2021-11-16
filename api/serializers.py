import datetime as dt

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, RoleChoices, Title, User


class UserSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user.role != RoleChoices.ADMIN:
            raise serializers.ValidationError("You are not admin to set roles")
        return value

    class Meta:
        fields = ("first_name",
                  "last_name",
                  "username",
                  "bio",
                  "email",
                  "role")
        model = User
        extra_kwargs = {
            "password": {"required": False},
            "email": {"required": True},
            "username": {"required": True},
        }


class RegistrationSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(
        source="password", required=False, write_only=True)
    username = serializers.CharField(
        required=False, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "confirmation_code"]


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    confirmation_code = serializers.CharField(source="password",
                                              max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email")
        confirmation_code = data.get("password")
        if email is None:
            raise serializers.ValidationError(
                "An email address is required to log in."
            )
        if confirmation_code is None:
            raise serializers.ValidationError(
                "A confirmation_code is required to log in."
            )
        user = authenticate(username=email, password=confirmation_code)
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and confirmation_code was not found."
            )
        if not user.is_active:
            raise serializers.ValidationError(
                "This user has been deactivated."
            )
        return {"token": user.token}


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        extra_kwargs = {
            "text": {"required": True},
            "score": {"required": True},
        }
        model = Review

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        author = self.context["request"].user
        title = self.context["view"].kwargs.get("title_id")
        if (Review.objects.filter(author=author, title=title).exists()
                and self.context["request"].method == "POST"):
            raise serializers.ValidationError(
                "Error: Review is already exists"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        extra_kwargs = {
            "text": {"required": True},
        }
        model = Comment

    def create(self, validated_data):
        print(self.context["request"].user.is_authenticated)
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id", )
        model = Genre

    def validate_name(self, value):
        if Genre.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Жанр с таким названием уже существует!"
            )
        return value

    def validate_slug(self, value):
        if Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                "Жанр с таким slug уже существует!"
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id", )
        model = Category

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Категория с таким названием уже существует!"
            )
        return value

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                "Категория с таким slug уже существует!"
            )
        return value


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.ListField(
        child=serializers.SlugRelatedField(slug_field='slug',
                                           required=False,
                                           queryset=Genre.objects.all()),
        allow_empty=True,
        write_only=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', required=False, queryset=Category.objects.all()
    )

    class Meta:
        fields = ("id", "name", "description",
                  "year", "genre", "category")
        extra_kwargs = {
            "name": {"required": True},
        }
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год создания!')
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(required=False, many=True, read_only=True)
    category = CategorySerializer(required=False, read_only=True)

    class Meta:
        fields = ("id", "name",
                  "rating", "description",
                  "year", "genre", "category")
        extra_kwargs = {
            "name": {"required": True},
        }
        model = Title
